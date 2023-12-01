"""
A module that calculates the rescaled range statistics for a given ticker.
This has been called the Mandelbrot Channel to pay homage to Benoit Mandelbrot
who popularized this framework in financial markets.
"""

from __future__ import annotations

import asyncio
import datetime as dt

import nest_asyncio
import polars as pl

from humbldata.core.helpers import DataToolHelpers as dth
from humbldata.core.helpers import MessageHelpers as mh
from humbldata.core.helpers import OpenBBHelpers as obbh
from humbldata.tools.mc.helpers import (
    add_rvol,
    cumdev,
    cumdev_range,
    cumdev_std,
    dataset_start,
    detrend,
    log_mean,
    price_range,
    vol_buckets,
)


class MandelbrotChannel:
    """
    A class used to represent the Mandelbrot Channel.

    Attributes
    ----------
    interval : int
        The interval for the Mandelbrot Channel, default is 1440.
    prepost : bool
        A flag indicating whether to include pre and post market data,
        default is False.
    source : str
        The source of the data, default is 'YahooFinance'.
    weekly : bool
        A flag indicating whether to use weekly data, default is False.
    monthly : bool
        A flag indicating whether to use monthly data, default is False.
    verbose : bool
        A flag indicating whether to print verbose messages for openbb
        obb.stocks.load() command, default is False.
    silent : bool
        A flag indicating whether to suppress all print statements,
        default is False.

    """

    def __init__(
        self,
        interval: str = "1d",
        prepost: bool = False,
        source: str = "yfinance",
        weekly: bool = False,
        monthly: bool = False,
        verbose: bool = False,
        silent: bool = False,
    ):
        self.interval = interval
        self.prepost = prepost
        self.source = source
        self.weekly = weekly
        self.monthly = monthly
        self.verbose = verbose
        self.silent = silent

    def calc_mc(
        self,
        symbol: str,
        fromdate: str | dt.datetime = "1950-01-01",
        todate: str | None = None,
        range: str = "1m",
        RS_method: str = "RS",
        live_price: bool = True,
        rvol_factor: bool = True,
        df: pl.LazyFrame | None = None,
        **kwargs,
    ) -> MandelbrotChannel:
        """
        Calculate the Mandelbrot Channel for a given stock symbol.

        Parameters
        ----------
        symbol : str
            The stock symbol to calculate the Mandelbrot Channel for.
        fromdate : Union[str, dt.datetime], optional
            The start date for the data collection, by default "1950-01-01".
        todate : Union[str, None], optional
            The end date for the data collection, by default None.
        range : str, optional
            The window range used in rescaled_range calculation, by default "1m"
        RS_method : str, optional
            The method used if fast is False, by default "RS".
        live_price : bool, optional
            If True, uses price from first stock data collection vs grabbing the
            most recent price, by default True.
        rvol_factor : bool, optional
            If True, used to select statistics from similar rvol buckets, by
            default True.
        df : Union[pl.LazyFrame, None], optional
            Used to pass in a dataframe instead of collecting data, useful in
            historical_mc(), by default None.
        **kwargs
            Additional parameters passed to:
            - `calculate_rvol()`:
                - rvol_method : str, optional
                    The method used to calculate rvol, by default "rolling".
                - window : int, optional
                    The window size for the rolling calculation, by default 21.
                - rv_mean : bool, optional
                    If True, uses the mean of the rolling window, by default
                    False.
            - `vol_buckets()`:
                - lo_quantile : float, optional
                    The lower quantile used in vol_buckets() method, by default
                    0.4.
                - hi_quantile : float, optional
                    The higher quantile used in vol_buckets() method, by default
                    0.8.

        Returns
        -------
        MandelbrotChannel
            Returns the MandelbrotChannel object with calculated top and bottom
            prices.

        Raises
        ------
        ValueError
            If the provided symbol is not found in the data.
        """
        # Store the settings for later use
        self.symbol = symbol
        self.range = range
        self.todate = todate
        self.live_price = live_price
        self.RS_method = RS_method
        self.rvol_factor = rvol_factor

        # Calculate starting date for dataset
        self.fromdate = dataset_start(
            range=self.range,
            fromdate=fromdate,
            todate=self.todate,
            return_dt=False,
        )

        # Step 1: Collect Price Data -------------------------------------------
        price_df = obbh.get_stock_prices(
            symbol=self.symbol,
            fromdate=self.fromdate,
            todate=self.todate,
            silent=True,
            lazy=True,
            df=df,
        )

        # Step 2: Calculate Log Returns + Rvol ---------------------------------
        price_df = dth.log_returns(df=price_df)

        # Step 3: Calculate Log Mean Series ------------------------------------
        log_mean_df = log_mean(df=price_df, window=range)

        # Step 4: Calculate Mean De-trended Series -----------------------------
        # Creates a merged dataframe with price_df data, and detrended mean
        out_df = detrend(df=price_df, mean_df=log_mean_df)

        # Step 5: Calculate Cumulative Deviate Series --------------------------
        out_df = cumdev(df=out_df)

        # Step 6: Calculate Mandelbrot Range -----------------------------------
        out_df = cumdev_range(df=out_df)

        # Step 7: Calculate Standard Deviation ---------------------------------
        out_df = cumdev_std(df=out_df)

        # Step 8: Calculate Range (R) & Standard Deviation (S) -----------------
        if rvol_factor:
            # Step 8.1: Calculate Realized Volatility --------------------------
            out_df = add_rvol(df=out_df, **kwargs)

            # Step 8.2: Return Volatility Bucket Stats (calculate vol buckets) -
            vol_stats = vol_buckets(
                df=out_df, lo_quantile=0.3, hi_quantile=0.65
            )

            # Step 8.3: Extract R & S ------------------------------------------
            R = vol_stats.select(pl.col("R")).collect().to_series()
            S = vol_stats.select(pl.col("S")).collect().to_series()
        else:
            # Step 8.1: Extract R & S ------------------------------------------
            R = out_df.select(pl.col("R")).collect().to_series()
            S = out_df.select(pl.col("S")).collect().to_series()

        RS = pl.Series("RS", R / S)
        RS_mean = RS.mean()  # noqa: F841
        RS_min = RS.min()  # noqa: F841
        RS_max = RS.max()  # noqa: F841

        # Step 10: Calculate Rescaled Price Range ------------------------------
        if live_price:
            recent_price = obbh.get_recent_price(symbol)  # noqa: F841
        else:
            recent_price = round(
                out_df.select(pl.col("adj_close"))
                .last()
                .collect()
                .rows()[0][0],
                4,
            )

        # Step 10.1: Extract Cumulative Deviate Max/Min Columns
        if rvol_factor:
            cumdev_max = (
                vol_stats.select(pl.col("cumdev_max")).collect().to_series()
            )
            cumdev_min = (
                vol_stats.select(pl.col("cumdev_min")).collect().to_series()
            )
        else:
            cumdev_max = (
                out_df.select(pl.col("cumdev_max")).collect().to_series()
            )
            cumdev_min = (
                out_df.select(pl.col("cumdev_min")).collect().to_series()
            )

        self.top_price, self.bottom_price = price_range(
            df=out_df,
            RS=RS,
            RS_mean=RS_mean,
            RS_max=RS_max,
            RS_min=RS_min,
            recent_price=recent_price,
            cumdev_max=cumdev_max,
            cumdev_min=cumdev_min,
            RS_method=RS_method,
            rvol_factor=rvol_factor,
        )

        if not self.silent:
            # Create the message
            mc_date = (
                out_df.tail(1).select("date").collect().to_series()[0].date()
            )

            mh.log_message(
                f"'[deep_sky_blue1]{range}[/deep_sky_blue1]' Mandelbrot Channel:\n Symbol: [green]{symbol}[/green] \n Date: [green]{mc_date}[/green] \n Bottom Range: [green]{self.bottom_price}[/green] -- Last Price: [green]{recent_price}[/green] -- Top Range: [green]{self.top_price}[/green]",
                "success",
            )

        return self

    async def _calc_mc_async(
        self, df: pl.DataFrame, **kwargs
    ) -> tuple[float, float, float]:
        """
        Asynchronously calculate the Mandelbrot Channel for a given stock symbol.

        Parameters
        ----------
        df : polars.DataFrame
            The dataframe containing the stock data.
        **kwargs
            Additional keyword arguments.

        Returns
        -------
        Tuple[float, float, float]
            The closing price, top price, and bottom price.
        """
        self.calc_mc(
            symbol=self.symbol,
            fromdate=self.fromdate,
            todate=self.todate,
            range=self.range,
            RS_method=self.RS_method,
            live_price=self.live_price,
            rvol_factor=self.rvol_factor,
            df=df,
            **kwargs,
        )
        close_price = (
            df.select(pl.col("adj_close")).last().collect().to_series()[0]
        )
        return close_price, self.top_price, self.bottom_price

    async def _historical_mc_engine(
        self,
        symbol: str,
        fromdate: str | dt.datetime = "1950-01-01",
        todate: str | None = None,
        range: str = "1m",
        RS_method: str = "RS",
        live_price: bool = True,
        rvol_factor: bool = True,
        df: pl.LazyFrame | None = None,
        **kwargs,
    ):
        """
        Calculate the Mandelbrot Channel for a given stock symbol, iterated
        over a range of dates to build a historical dataset.

        Parameters
        ----------
        symbol : str
            The stock symbol to calculate the Mandelbrot Channel for.
        fromdate : Union[str, dt.datetime], optional
            The start date for the data collection, by default "1950-01-01".
        todate : Union[str, None], optional
            The end date for the data collection, by default None.
        range : str, optional
            The window range used in rescaled_range calculation, by default "1m".
        RS_method : str, optional
            The method used if fast is False, by default "RS".
        live_price : bool, optional
            If True, uses price from first stock data collection vs grabbing the
            most recent price, by default True.
        rvol_factor : bool, optional
            If True, used to select statistics from similar rvol buckets, by
            default True.
        df : Union[pl.LazyFrame, None], optional
            Used to pass in a dataframe instead of collecting data, useful in
            historical_mc(), by default None.
        **kwargs
            Additional parameters passed to:
            - `calculate_rvol()`:
                - rvol_method : str, optional
                    The method used to calculate rvol, by default "rolling".
                - window : int, optional
                    The window size for the rolling calculation, by default 21.
                - rv_mean : bool, optional
                    If True, uses the mean of the rolling window, by default
                    False.
            - `vol_buckets()`:
                - lo_quantile : float, optional
                    The lower quantile used in vol_buckets() method, by default
                    0.1.
                - hi_quantile : float, optional
                    The higher quantile used in vol_buckets() method, by default
                    0.9.

        Returns
        -------
        pl.DataFrame
            Returns a pl.DataFrame object with historical Mandelbrot Channel
            data.

        Raises
        ------
        ValueError
            If the provided symbol is not found in the data.
        """
        # Store the settings for later use in historical()
        self.symbol = symbol
        self.range = range
        self.todate = todate
        self.live_price = live_price
        self.RS_method = RS_method
        self.rvol_factor = rvol_factor

        # Calculate starting date for dataset
        self.fromdate = dataset_start(
            range=self.range,
            fromdate=fromdate,
            todate=self.todate,
            return_dt=False,
        )

        # Generate a list of dates between fromdate and todate
        start = dt.datetime.strptime(self.fromdate, "%Y-%m-%d").date()
        end = dt.datetime.strptime(self.todate, "%Y-%m-%d").date()
        dates = pl.date_range(start=start, end=end, eager=True, name="date")
        # Step 1: Collect Price Data -------------------------------------------
        price_df = obbh.get_stock_prices(
            symbol=self.symbol,
            fromdate=self.fromdate,
            todate=self.todate,
            silent=True,
            lazy=True,
            df=df,
        )

        # Step 2: Create a list of tasks ---------------------------------------
        tasks = [
            asyncio.create_task(
                self._calc_mc_async(
                    df=price_df.filter(pl.col("date") <= date), **kwargs
                )
            )
            for date in dates
        ]
        # Gather the results of all tasks
        results = await asyncio.gather(*tasks)
        # Convert the results to a Polars DataFrame
        symbol_column = [symbol] * len(dates)
        out_df = pl.DataFrame(
            {
                "date": dates,
                "symbol": symbol_column,
                "mc_lo": [result[2] for result in results],
                "adj_close": [result[0] for result in results],
                "mc_hi": [result[1] for result in results],
            }
        )
        return out_df

    def historical_mc(
        self,
        symbol: str,
        fromdate: str | dt.datetime = "1950-01-01",
        todate: str | None = None,
        range: str = "1m",
        RS_method: str = "RS",
        live_price: bool = True,
        rvol_factor: bool = True,
        df: pl.LazyFrame | None = None,
        **kwargs,
    ):
        """
        Calculate the Mandelbrot Channel for a given stock symbol, iterated
        over a range of dates to build a historical dataset.

        Parameters
        ----------
        symbol : str
            The stock symbol to calculate the Mandelbrot Channel for.
        fromdate : Union[str, dt.datetime], optional
            The start date for the data collection, by default "1950-01-01".
        todate : Union[str, None], optional
            The end date for the data collection, by default None.
        range : str, optional
            The window range used in rescaled_range calculation, by default "1m".
        RS_method : str, optional
            The method used if fast is False, by default "RS".
        live_price : bool, optional
            If True, uses price from first stock data collection vs grabbing the
            most recent price, by default True.
        rvol_factor : bool, optional
            If True, used to select statistics from similar rvol buckets, by
            default True.
        df : Union[pl.LazyFrame, None], optional
            Used to pass in a dataframe instead of collecting data, useful in
            historical_mc(), by default None.
        **kwargs
            Additional parameters passed to:
            - `calculate_rvol()`:
                - rvol_method : str, optional
                    The method used to calculate rvol, by default "rolling".
                - window : int, optional
                    The window size for the rolling calculation, by default 21.
                - rv_mean : bool, optional
                    If True, uses the mean of the rolling window, by default
                    False.
            - `vol_buckets()`:
                - lo_quantile : float, optional
                    The lower quantile used in vol_buckets() method, by default
                    0.4.
                - hi_quantile : float, optional
                    The higher quantile used in vol_buckets() method, by default
                    0.8.

        Returns
        -------
        pl.DataFrame
            Returns a pl.DataFrame object with historical Mandelbrot Channel
            data.

        Raises
        ------
        ValueError
            If the provided symbol is not found in the data.
        """
        nest_asyncio.apply()
        return asyncio.run(
            self._historical_mc_engine(
                symbol=symbol,
                fromdate=fromdate,
                todate=todate,
                range=range,
                RS_method=RS_method,
                live_price=live_price,
                rvol_factor=rvol_factor,
                df=df,
                **kwargs,
            )
        )
