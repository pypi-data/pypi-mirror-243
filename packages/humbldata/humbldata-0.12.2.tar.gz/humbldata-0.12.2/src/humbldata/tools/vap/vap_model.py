"""
A module that calculates the volatility adjusted premium for a given ticker.
This is the volatility +premium OR -discount between the realized volatility 
and the implied volatility.
"""

import pandas as pd
import polars as pl

from humbldata.core.helpers import OpenBBHelpers as obbh
from humbldata.core.helpers import PanderaHelpers as pah
from humbldata.core.models.abstract.errors import HumblDataError
from humbldata.core.models.stocks_model import StocksBaseModel
from humbldata.orats.data import OratsData
from humbldata.tools.vap.helpers import (
    check_iv_endpoint,
    data_alignment,
    format_date,
    merge_data,
    plot_engine,
    vap_engine,
    vap_performance_engine,
    vap_signal_engine,
)
from humbldata.volatility.estimators import VolatilityEstimators


class VolatilityPremium:
    def __init__(
        self,
        silent: bool = False,
        clean: bool = True,
    ):
        self.silent = silent
        self.clean = clean

    def calc_vap(
        self,
        rvol_method: str,
        iv_endpoint: str,
        ticker: str,
        fromdate: str = "2007-01-03",
        todate: str | None = None,  # default set to today
        price_data: pl.DataFrame | pd.DataFrame | None = None,
        vol_window: int = 30,
        trading_periods: int = 252,
        rv_calc_column: str = "Volatility_mean",
        iv_calc_column: str = "iv",
        rv_mean: bool = True,
        **kwargs,
    ):
        """
        Description:
        ------------
        Calculate the volatility premium for a given ticker.
        This is the difference between the realized volatility and the implied
        volatility.
        This function uses the VolatilityEstimators class to calculate the
        Realized Volatility, and the OratsData class to calculate the Implied
        Volatility.
        Params:
        -------
        - rvol_method : str, required
            The volatility estimator to use.
        - iv_endpoint : str, required
            The endpoint to use for the implied volatility. Valid options are
            "strikesHistory", "ivRankHistory", "summariesHistory",
            "coreDataHistory". See the OratsData class for more info.
        - ticker : str, required
            The ticker to use for the implied volatility.
        - fromdate : str, optional
            The start date to use for the implied volatility. Defaults to
            2007-01-03.
        - todate : str, optional
            The end date to use for the implied volatility. Defaults to today's
            date
        - price_data : pl.DataFrame, optional
            The price data to use. Defaults to None. If None, you must supply
            fromdate, todate, and ticker to collect from openbb.
        - vol_window : int, optional
            The window to use for the volatility estimators. Defaults to 30.
        - trading_periods : int, optional
            The number of trading periods to use for the volatility estimators.
            Defaults to 252.
        - rv_calc_column : str, optional
            The column to use for the realized volatility. Defaults to
            'Volatility_mean', when `rv_mean=True` .This will depend on what
            rvol_method you use, and if `rv_mean=False`.
            - RV_COLUMNS when rv_mean is False:
                - orats_hv: clsHv10d, clsHv20d, clsHv30d
                - std: Volatility_pct
                - parkinson: Volatility_pct
                - garman_klass: Volatility_pct
                - hodges_tompkins: Volatility_pct
                - rogers_satchell: Volatility_pct
                - yang_zhang: Volatility_pct
                - squared_returns: Volatility_pct
        - iv_calc_column : str, optional
            The column to use for the implied volatility. Defaults to 'iv'.
            This will depend on what iv_endpoint you use.
            - IV_COLUMNS:
                - ivRankHistory: iv
                - summariesHistory: iv30d, exErnIv30d, fwd60_30
                - coreDataHistory: atmIvM1, atmIvM2, atmIvM3, atmIvM4, iv30d
        - rv_mean : bool, optional
            If True, the mean of the 10,20,30D realized volatility will be
            used in the vol_premia calculation. Defaults to True.
        - **kwargs : dict
            A dictionary of keyword arguments to pass to the function.
            - If you don't supply price_data OR if you use 'orats_hv'.
            Data collection will default to 2007-01-01 to today's date.
            You must pass the `fromdate`, `todate` if you want specific dates
        Returns:
        --------
        `Self` Object:
        Assigns .price_data & .merged_data to object
        """
        # Setup ----------------------------------------------------------------
        # Assign Ticker
        self.ticker = ticker

        # Assign Default Dates (assigns today if date is None)
        self.todate = format_date(todate)
        self.fromdate = format_date(fromdate)

        # Assign Price Data
        self.price_data = obbh.get_stock_prices(
            symbol=self.ticker,
            df=price_data,
            fromdate=self.fromdate,
            todate=self.todate,
            silent=self.silent,
            provider="fmp",
        )
        # Step 1: Calculate Realized Volatility --------------------------------
        # Initialize VolatilityEstimators class
        vol = VolatilityEstimators(clean=True, silent=self.silent)
        rvol = vol.calculate_rvol(
            rvol_method=rvol_method,
            price_data=self.price_data,
            window=vol_window,
            trading_periods=trading_periods,
            ticker=ticker,
            fromdate=self.fromdate,
            todate=self.todate,
            rv_mean=rv_mean,
        )
        # Step 2: Calculate Implied Volatility ---------------------------------
        check_iv_endpoint(iv_endpoint)
        # Instantiate OratsData class
        orats = OratsData(silent=self.silent)
        # Collect Implied Volatility Data
        ivol = orats.get_data(iv_endpoint, ticker, self.fromdate, self.todate)

        # Step 3: Align Series -------------------------------------------------
        rvol, ivol = data_alignment(rvol, ivol)
        # Step 4: Calculate Volatility Premium ---------------------------------
        premia = vap_engine(
            rvol_method=rvol_method,
            iv_endpoint=iv_endpoint,
            ivol_df=ivol,
            rvol_df=rvol,
            iv_calc_column=iv_calc_column,
            rv_calc_column=rv_calc_column,
            rv_mean=rv_mean,
            clean=self.clean,
        )

        # Step 5: Merge price_data and premia_data -----------------------------
        self.merged_data = merge_data(
            self=self, price_data=self.price_data, premia_data=premia
        )
        # Assign Plot Variable to Self, this changes if .performance()/.signal()
        self.plot_method = "simple"

        return self

    def signal(
        self,
        price_data: pl.DataFrame | pd.DataFrame | None = None,
        premia_data: pl.DataFrame | pd.DataFrame | None = None,
        roc_periods: int = 1,
        roc_order: int = 1,
        **kwargs,
    ):
        """
        This method generates the VAP signal,
        subsets the data, and calculates performance stats.

        Parameters
        ----------
        price_data : pl.DataFrame | pd.DataFrame | None, optional
            The price data to be used. If None, the price data from the instance
            is used.
        premia_data : pl.DataFrame | pd.DataFrame | None, optional
            The premia data to be used. If None, the premia data from the
            instance is used.
        roc_periods : int, optional
            The number of periods to use for the rate of change. Defaults to 1.
        roc_order : int, optional
            The order of the rate of change. Defaults to 1.
            If the order is 2, this is the ROC of the ROC

        **kwargs
            Additional keyword arguments to be passed to the vap_signal_engine
            function.

        Details
        -------
        ### **kwargs:
        ##### _percentile options :
                - `signal_method` : str, 'rolling' OR 'growing'
                - `window` : int, the window to use for 'rolling' calculations

        ##### _quantiles options :
                - `signal_method` : str, 'rolling' OR 'growing'
                - `window` : int, the window to use for 'rolling' calculations
                - `quantiles : Tuple[float,float]` , ie (0.2,0.8)

        Returns
        -------
        self
            Returns the instance itself.

            Assigns .signal_gross/degross

        Examples
        --------
        >>> signal(price_data=price_df, premia_data=premia_df)
        """
        # Step 1: Calculate Signal ---------------------------------------------
        self.merged_data = vap_signal_engine(
            data=self.merged_data,
            roc_column="premia_pct",
            roc_period=roc_periods,
            roc_order=roc_order,
            roc_pct=False,
            **kwargs,
        )
        # Step 2: Subset Data --------------------------------------------------
        self.signal_degross = self.merged_data.filter(pl.col("degross_fired"))
        self.signal_gross = self.merged_data.filter(pl.col("gross_fired"))
        # DONE -----------------------------------------------------------------
        self.plot_method = "signal"
        return self

    def performance(self, **kwargs):
        """
        Calculates trade performance based on .signal_gross/degross generated in
        .signal()
        Executes the vap_performance_engine function with the provided keyword
        arguments.
        Sets the plot_method attribute to "performance".

        Parameters
        ----------
        - **kwargs : Additional keyword arguments to be passed to the
        vap_performance_engine function.
            - `reinvest` : int, 0 or 1, default 1. The percentage of capital to
            reinvest
            - `init_investment` : float, default 100. Initial investment

        Returns
        -------
        self
            Assigns .trade_data & .trade_stats

        Examples
        --------
        >>> performance(kwargs={'reinvest': 1, 'init_investment': 100})
        """
        vap_performance_engine(self, **kwargs)
        self.plot_method = "performance"
        return self

    def plot(self, show: bool = False):
        """
        Executes the plot engine function with the provided show parameter.
        Sets the plot and perf_plot attributes.

        Parameters
        ----------
        show : bool
            Controls the fig.show() code. You do not want to show
            plot in a webapp, they will open new tabs.

        Returns
        -------
        self
            Returns the instance of the class.
            .plot: VAP plot
            .perf_plot: strategy performance plot

        Examples
        --------
        >>> plot(show=True)
        """
        self = plot_engine(self=self, plot_method=self.plot_method, show=show)
        return self

    def get_price_data(self) -> pl.DataFrame:
        """
        Validates and Returns the price data.

        Returns
        -------
        pl.DataFrame
            The price data.
        """
        df = self.price_data.collect().to_pandas()
        StocksBaseModel.validate(df)

        return self.price_data.collect()

    def get_merged_data(self) -> pl.DataFrame:
        """
        Validates and Returns the merged data.

        Returns
        -------
        pl.DataFrame
            The merged data.
        """
        return self.merged_data.collect()

    def get_trade_data(self) -> pl.DataFrame:
        """
        Validates and Returns the trade data.

        Returns
        -------
        pl.DataFrame
            The trade data.
        """
        if self.trade_data is None:
            raise HumblDataError(
                "Trade data is not available. Please call the 'performance' method first."
            )
        return self.trade_data.collect()

    def get_trade_stats(self) -> pl.DataFrame:
        """
        Validates and Returns the trade statistics.

        Returns
        -------
        pl.DataFrame
            The trade statistics.
        """
        if self.trade_stats is None:
            raise HumblDataError(
                "Trade statistics are not available. Please call the 'performance' method first."
            )
        return self.trade_stats.collect()

    def get_signal_gross(self) -> pl.DataFrame:
        """
        Validates and Returns the signal_gross data.

        Returns
        -------
        pl.DataFrame
            The signal_gross data.
        """
        if self.signal_gross is None:
            raise HumblDataError(
                "Signal gross data is not available. Please call the 'performance' method first."
            )
        return self.signal_gross.collect()

    def get_signal_degross(self) -> pl.DataFrame:
        """
        Validates and Returns the signal_degross data.

        Returns
        -------
        pl.DataFrame
            The signal_degross data.
        """
        if self.signal_degross is None:
            raise HumblDataError(
                "Signal degross data is not available. Please call the 'performance' method first."
            )
        return self.signal_degross.collect()
