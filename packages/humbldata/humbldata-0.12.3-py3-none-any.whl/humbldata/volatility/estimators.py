"""A group of various different volatility estimators."""
import datetime as dt
import inspect
import math

import numpy as np
import pandas as pd
import polars as pl

from humbldata.core.constants import RV_METHODS
from humbldata.core.helpers import DataFrameHelpers as dfh
from humbldata.core.helpers import DataToolHelpers as dth
from humbldata.core.helpers import MessageHelpers
from humbldata.core.helpers import OpenBBHelpers as obbh
from humbldata.core.models.abstract.errors import HumblDataError
from humbldata.core.models.stocks_model import StocksBaseModel
from humbldata.orats.data import OratsData


class VolatilityEstimators:
    def __init__(
        self,
        clean: bool = True,
        silent: bool = False,
    ):
        """
        Initialize the VolatilityEstimators object.

        Params:
        -------
        - clean : bool, optional
            A flag indicating whether to drop NaN values from the df
            (True) or not (False). Defaults to True.
        - silent : bool, optional
            A flag indicating whether to suppress messages (True) or not
            Defaults to False.
        """
        self.clean = clean
        self.silent = silent

        # Setting these to None to avoid errors, used in _rvol_engine
        self.price_data = None
        self.window = None
        self.trading_periods = None
        self.pl_convert = None
        self.rv_mean = None

    def calculate_rvol(
        self,
        price_data: pd.DataFrame | pl.DataFrame | pl.LazyFrame,
        rvol_method: str = "orats_hv",
        window=30,
        trading_periods=252,
        **kwargs,
    ) -> pl.LazyFrame:
        """
        The main  parent function to compile all the volatility estimators. You
        can supply prices_data or use the default of None and supply ticker,
        fromdate, and todate to collect from openbb. You can change the
        rvol_method used to calculated volatility. Using 'orats_hv' will require
        ticker, fromdate, and todate to be supplied. This function automatically
        calculates the realized volatility mean of 10D, 20D, 30D, unless you
        specify otherwise. Please see _rvol_engine for more info.

        --------
        Params:
        rvol_method : str
            The volatility estimator to use. Available options are:
            - std
            - parkinson
            - garman_klass
            - hodges_tompkins
            - rogers_satchell
            - yang_zhang
            - squared_returns
            - orats_hv (you must supply ticker, fromdate and todate if using)
        price_data : pl.DataFrame, optional
            The price data to use. Defaults to None.

        **kwargs : tuple
            The arguments to pass to the function if price_data is None.
            You must pass the ticker, fromdate, and todate. This will collect
            and create a pl.DataFrame from openbb.
            You must supply ticker, fromdate and todate if using `orats_hv` or
            don't provide price_data.
            - You can also supply `rv_mean = False` if you do not want to
            calculate the mean of 10D, 20D, 30D volatility
        Returns:
        --------


        """
        # Init Classes ---------------------------------------------------------
        m = MessageHelpers.log_message

        # Step 1: Run Parameter logic ------------------------------------------
        # Used for side-effect self assigns, configure price_data object
        self._rvol_engine(
            rvol_method, price_data, window, trading_periods, **kwargs
        )

        # Step 2: Choose Volatility Estimator ----------------------------------
        rvol_fct = getattr(self, f"_{rvol_method}")

        m(
            f"Calculating <{rvol_method}> volatility...",
            "info",
            self.silent,
        )

        # Step 3: Calculate Volatility -----------------------------------------
        try:
            result = rvol_fct(
                self.price_data, self.window, self.trading_periods, self.clean
            )
            m(
                f"Finished calculating <{rvol_method}> volatility!",
                "success",
                self.silent,
            )

            return result
        except Exception as e:
            parent_func = inspect.currentframe().f_code.co_name
            raise HumblDataError(
                f"""Error in `{parent_func}()`:
                Issue arose calculating volatility with `{rvol_fct.__name__}` method!

                ------------------- ERROR -------------------
                {str(e)}"""
            ) from e

    def _rvol_engine(
        self,
        rvol_method: str,
        price_data: pl.DataFrame | pd.DataFrame | pl.LazyFrame,
        window=30,
        trading_periods=252,
        **kwargs,
    ):
        """
        The main logic behind calculate_rvol. Used to decide what endpoint is
        being used and if price_data is empty. This will determine if we need
        fromdate, todate, and ticker to collect new data from openbb.

        This function automatically assigns rv_mean to True, unless the user
        sends in rv_mean = False in kwargs. Default behavior is to calculate
        the realized volatility mean of 10D, 20D, 30D.

        Params:
        -------
        - rvol_method : str, required
            The volatility estimator to use.
        - price_data : pd.DataFrame, optional
            The price data to use. Defaults to None. If None, you must supply
            fromdate, todate, and ticker to collect from openbb.
        - window : int, optional
            The window to use for the volatility estimators. Defaults to 30.
        - trading_periods : int, optional
            The number of trading periods to use for the volatility estimators.
            Defaults to 252.
        - **kwargs : dict
            A dictionary of keyword arguments to pass to the function if
            you don't supply price_data OR if you use 'orats_hv'.
            You must pass:
                - `ticker`
                - `fromdate`
                - `todate`
            If you only pass `ticker`, `fromdate`, and `todate`, will default to
            2007-01-01 --> today.
            Please pass `rv_mean = False` if you do not want to calculate the
            realized volatility mean of 10D, 20D, 30D.
        """
        self.price_data = price_data
        self.window = window
        self.trading_periods = trading_periods
        self.pl_convert = dfh.to_polars_safe

        # Check rvol_method ----------------------------------------------------
        if rvol_method not in RV_METHODS:
            raise ValueError(
                f"Invalid option '{rvol_method}'. Available options are "
                f"{RV_METHODS}."
            )
        # Require ticker, fromdate, and todate if using orats_hv or no
        # price_data, to collect from obb
        if self.price_data is None or rvol_method == "orats_hv":
            try:
                self.ticker = kwargs["ticker"]
                self.fromdate = kwargs.get("fromdate", "2007-01-03")
                self.todate = kwargs.get(
                    "todate", dt.date.today().strftime("%Y-%m-%d")
                )
            except KeyError as e:
                raise ValueError(
                    "If price_data is not provided OR rvol_method = 'orats_hv'"
                    " 'ticker', 'fromdate', and 'todate' MUST be provided."
                ) from e
        # Determine rv_mean logic, default is True, will change if user passes F
        self.rv_mean = kwargs.get("rv_mean", True)

        # If price_data is available and not formatted, and rvol_method is not 'orats_hv'
        if (
            self.price_data is not None
            and not hasattr(self.price_data, "_formatted")
            and rvol_method != "orats_hv"
        ):
            # Convert price_data to_dict based on its type (LazyFrame/DataFrame)
            if isinstance(self.price_data, pl.LazyFrame):
                self.price_data = self.price_data.collect().to_pandas()
            elif isinstance(self.price_data, pd.DataFrame):
                pass
            else:
                self.price_data = self.price_data.to_pandas()

            # Validate the data
            self.price_data = StocksBaseModel(self.price_data)

            # Return to pl.LazyFrame
            self.price_data = pl.from_pandas(self.price_data).lazy()

            # Set _formatted to True to avoid reformatting
            self.price_data._formatted = True

        # If price_data is not available and rvol_method is not 'orats_hv'
        elif self.price_data is None and rvol_method != "orats_hv":
            # Load and format the data
            self.price_data = StocksBaseModel(
                obbh.get_stock_prices(
                    symbol=self.ticker,
                    fromdate=self.fromdate,
                    todate=self.todate,
                    silent=self.silent,
                    lazy=False,
                ).to_pandas()
            )
            self.price_data = pl.from_pandas(self.price_data).lazy()

    def _annual_vol(self, s):
        """
        The function f(s) is a user-defined function that takes a Polars Series
        `s` as input. This function calculates the square root of the product of
        trading_periods and the mean of the series s.
        ------
        Params:
        -------
        s : Polars Series
            A series to calculate the annual volatility from.
        ### Context:

        In the  of the Parkinson and Garman-Klass and Rogers Satchell
        volatility estimators, this function is used to calculate the annualized
        volatility. Here's a breakdown of what it does:

        1. s.mean(): This calculates the average of the series s. In the context
        of the Parkinson and Garman-Klass volatility estimators, s would be a
        series of daily volatility measures.

        2. trading_periods * s.mean(): This scales the average daily volatility
        by the number of trading periods in a year to annualize it. The variable
        trading_periods typically takes a value of 252, which is the average
        number of trading days in a year.

        3. (trading_periods * s.mean()) ** 0.5: This takes the square root of
        the annualized volatility. The square root is used because volatility is
        typically defined as the standard deviation of returns, and the standard
        deviation is the square root of the variance.

        So overall, the function f(s) is used to calculate the annualized
        volatility from a series of daily volatility measures.
        """
        trading_periods = self.trading_periods
        return (trading_periods * s.mean()) ** 0.5

    def _std(self, price_data, window=30, trading_periods=252, clean=True):
        """
        Standard deviation calculation. Standard deviation measures how widely
        returns are dispersed from the average return. It is the most common
        (and biased) estimator of volatility.
        """
        price_data = dth.log_returns(df=price_data)

        # RV_MEAN - lazyAPI execution
        if self.rv_mean is True:
            results = []
            windows = [10, 20, 30]
            for window in windows:
                result = price_data.with_columns(
                    (
                        pl.col("log_returns").rolling_std(
                            window_size=window, min_periods=1
                        )
                        * math.sqrt(trading_periods)
                        * 100
                    ).alias(f"Volatility_pct_{window}D")
                )
                results.append(result)

            # Combine results into a single lazyFrame
            result = pl.concat(results, how="align")
            vol_cols = [f"Volatility_pct_{window}D" for window in windows]
            result = result.with_columns(
                result.select(pl.col(vol_cols))
                .collect()
                .mean(axis=1)
                .alias("Volatility_mean")
            ).lazy()

        else:
            result = price_data.with_columns(
                (
                    pl.col("log_returns").rolling_std(
                        window_size=window, min_periods=1
                    )
                    * math.sqrt(trading_periods)
                    * 100
                ).alias("Volatility_pct")
            )
        if clean:
            return result.drop_nulls()
        else:
            return result

    def _parkinson(
        self, price_data, window=30, trading_periods=252, clean=True
    ):
        """
        Parkinson’s volatility uses the stock’s high and low price of the day
        rather than just close to close prices. It’s useful to capture large
        price movements during the day.
        """
        # Need pl.DataFrame for this logic
        price_data = price_data.collect()
        rs = (1.0 / (4.0 * math.log(2.0))) * (
            (price_data["high"] / price_data["low"]).map_elements(
                np.log, return_dtype=pl.Float64
            )
        ) ** 2.0

        # RV_MEAN LOGIC
        if self.rv_mean is True:
            results = []
            windows = [10, 20, 30]
            for window in windows:
                result = price_data.with_columns(
                    (
                        rs.rolling_map(
                            self._annual_vol, window_size=window, min_periods=1
                        )
                        * 100
                    ).alias(f"Volatility_pct_{window}D")
                )
                results.append(result)

            # Combine results into a single lazyFrame
            result = pl.concat(results, how="align")
            vol_cols = [f"Volatility_pct_{window}D" for window in windows]
            result = result.with_columns(
                result.select(pl.col(vol_cols))
                .mean(axis=1)
                .alias("Volatility_mean")
            )

        else:
            result = price_data.with_columns(
                (
                    rs.rolling_map(
                        self._annual_vol, window_size=window, min_periods=1
                    )
                    * 100
                ).alias("Volatility_pct")
            )

        if clean:
            return result.drop_nulls().lazy()
        else:
            return result.lazy()

    def _garman_klass(
        self, price_data, window=30, trading_periods=252, clean=True
    ):
        """
        Garman-Klass volatility extends Parkinson’s volatility by taking into
        account the opening and closing price. As markets are most active during
        the opening and closing of a trading session, it makes volatility
        estimation more accurate.
        """

        price_data = price_data.collect()

        log_hl = (price_data["high"] / price_data["low"]).log()
        log_co = (price_data["adj_close"] / price_data["open"]).log()

        rs = 0.5 * log_hl**2 - (2 * np.log(2) - 1) * log_co**2

        # HOTFIX START ---------------------------------------------------------
        rs = rs.to_pandas()

        if self.rv_mean is True:
            results = []
            windows = [10, 20, 30]
            for window in windows:
                # result = price_data.with_columns(
                #     (
                #         rs.rolling_map(
                #             self._annual_vol, window_size=window, min_periods=1
                #         )
                #         * 100
                #     ).alias(f"Volatility_pct_{window}D")
                # )

                # Calculate Rolling Volatility (in Pandas)
                result = (
                    rs.rolling(
                        window=window, center=False, min_periods=2
                    ).apply(func=self._annual_vol)
                    * 100
                )

                # Add column to df (in Polars)
                result = price_data.with_columns(
                    pl.Series(f"Volatility_pct_{window}D", result)
                )

                # Append to results
                results.append(result)

            # Combine results into a single lazyFrame
            result = pl.concat(results, how="align")
            vol_cols = [f"Volatility_pct_{window}D" for window in windows]
            result = result.with_columns(
                result.select(pl.col(vol_cols))
                .mean(axis=1)
                .alias("Volatility_mean")
            )

        else:
            # result = price_data.with_columns(
            #     (
            #         rs.rolling_map(
            #             self._annual_vol, window_size=window, min_periods=1
            #         )
            #         * 100
            #     ).alias("Volatility_pct")
            # )
            result = (
                rs.rolling(window=window, center=False, min_periods=2).apply(
                    func=self._annual_vol
                )
                * 100
            )

            # Add column to df (in Polars)
            result = price_data.with_columns(
                pl.Series("Volatility_pct", result)
            )

        # HOTFIX END -----------------------------------------------------------

        if clean:
            return result.drop_nulls().lazy()
        else:
            return result.lazy()

    def _hodges_tompkins(
        self, price_data, window=30, trading_periods=252, clean=True
    ):
        """
        Hodges-Tompkins volatility is a bias correction for estimation using an
        overlapping data sample that produces unbiased estimates and a
        substantial gain in efficiency.
        """
        price_data = price_data

        price_data = dth.log_returns(df=price_data)

        # When calculating rv_mean, need a different adjustment factor,
        # so window doesn't influence the Volatility_mean

        # RV_MEAN
        if self.rv_mean is True:
            results = []
            windows = [10, 20, 30]
            for window in windows:
                # Calculate Adjustment Factor
                vol = price_data.with_columns(
                    (
                        pl.col("log_returns").rolling_std(
                            window_size=window, min_periods=1
                        )
                        * np.sqrt(trading_periods)
                    ).alias("vol")
                ).select(pl.col("vol"))

                h = window
                count = price_data.select(pl.count("log_returns")).collect()[
                    0, 0
                ]
                n = (count - h) + 1

                adj_factor = 1.0 / (
                    1.0 - (h / n) + ((h**2 - 1) / (3 * n**2))
                )

                result = price_data.with_columns(
                    ((vol.collect() * adj_factor) * 100)
                    .to_series()
                    .alias(f"Volatility_pct_{window}D")
                )
                results.append(result)

            # Combine results into a single lazyFrame
            result = pl.concat(results, how="align")
            vol_cols = [f"Volatility_pct_{window}D" for window in windows]
            result = result.with_columns(
                result.select(pl.col(vol_cols))
                .collect()
                .mean(axis=1)
                .alias("Volatility_mean")
            )

        else:
            vol = price_data.with_columns(
                (
                    pl.col("log_returns").rolling_std(
                        window_size=window, min_periods=1
                    )
                    * np.sqrt(trading_periods)
                ).alias("vol")
            ).select(pl.col("vol"))

            h = window
            count = price_data.select(pl.count("log_returns")).collect()[0, 0]
            n = (count - h) + 1

            adj_factor = 1.0 / (1.0 - (h / n) + ((h**2 - 1) / (3 * n**2)))

            result = price_data.with_columns(
                ((vol.collect() * adj_factor) * 100)
                .to_series()
                .alias("Volatility_pct")
            )
        if clean:
            return result.drop_nulls()
        else:
            return

    def _rogers_satchell(
        self, price_data, window=30, trading_periods=252, clean=True
    ):
        """
        Rogers-Satchell is an estimator for measuring the volatility of
        securities with an average return not equal to zero. Unlike Parkinson
        and Garman-Klass estimators, Rogers-Satchell incorporates a drift term
        (mean return not equal to zero).
        """
        price_data = price_data.with_columns(
            [
                (pl.col("high") / pl.col("open")).log().alias("log_ho"),
                (pl.col("low") / pl.col("open")).log().alias("log_lo"),
                (pl.col("adj_close") / pl.col("open")).log().alias("log_co"),
            ]
        ).with_columns(
            (
                pl.col("log_ho") * (pl.col("log_ho") - pl.col("log_co"))
                + pl.col("log_lo") * (pl.col("log_lo") - pl.col("log_co"))
            ).alias("rs")
        )

        # RV_MEAN
        if self.rv_mean is True:
            results = []
            windows = [10, 20, 30]
            for window in windows:
                result = price_data.with_columns(
                    (
                        pl.col("rs").rolling_map(
                            self._annual_vol, window_size=window, min_periods=1
                        )
                        * 100
                    ).alias(f"Volatility_pct_{window}D")
                )
                results.append(result)

            # Combine results into a single DataFrame (pl.concat converts)
            result = pl.concat(results, how="align")
            vol_cols = [f"Volatility_pct_{window}D" for window in windows]
            result = result.with_columns(
                result.select(pl.col(vol_cols))
                .collect()
                .mean(axis=1)
                .alias("Volatility_mean")
            ).lazy()

        else:
            result = price_data.with_columns(
                (
                    pl.col("rs").rolling_map(
                        self._annual_vol, window_size=window, min_periods=1
                    )
                    * 100
                ).alias(f"Volatility_pct_{window}D")
            )

        if clean:
            return result.drop_nulls()
        else:
            return result

    def _yang_zhang(
        self, price_data, window=30, trading_periods=252, clean=True
    ):
        """
        Yang-Zhang volatility is the combination of the overnight
        (close-to-open volatility), a weighted average of the Rogers-Satchell
        volatility and the day’s open-to-close volatility.
        """
        price_data = price_data.with_columns(
            [
                (pl.col("high") / pl.col("open")).log().alias("log_ho"),
                (pl.col("low") / pl.col("open")).log().alias("log_lo"),
                (pl.col("adj_close") / pl.col("open")).log().alias("log_co"),
                (pl.col("open") / pl.col("adj_close").shift())
                .log()
                .alias("log_oc"),
                (pl.col("adj_close") / pl.col("adj_close").shift())
                .log()
                .alias("log_cc"),
            ]
        ).with_columns(
            [
                (pl.col("log_oc") ** 2).alias("log_oc_sq"),
                (pl.col("log_cc") ** 2).alias("log_cc_sq"),
                (
                    pl.col("log_ho") * (pl.col("log_ho") - pl.col("log_co"))
                    + pl.col("log_lo") * (pl.col("log_lo") - pl.col("log_co"))
                ).alias("rs"),
            ]
        )

        # RV_MEAN
        if self.rv_mean is True:
            results = []
            windows = [10, 20, 30]
            for window in windows:
                k = 0.34 / (1.34 + (window + 1) / (window - 1))
                price_data_mean = self._yang_zhang_engine(
                    price_data=price_data,
                    window=window,
                    trading_periods=trading_periods,
                )
                result = price_data_mean.with_columns(
                    (
                        (
                            pl.col("open_vol")
                            + k * pl.col("close_vol")
                            + (1 - k) * pl.col("window_rs")
                        ).sqrt()
                        * np.sqrt(trading_periods)
                        * 100
                    ).alias(f"Volatility_pct_{window}D")
                ).select(
                    pl.exclude(
                        [
                            "log_ho",
                            "log_lo",
                            "log_co",
                            "log_oc",
                            "log_cc",
                            "log_oc_sq",
                            "log_cc_sq",
                            "rs",
                            "close_vol",
                            "open_vol",
                            "window_rs",
                        ]
                    )
                )
                results.append(result)

            # Combine results into a single lazyFrame
            result = pl.concat(results, how="align")
            vol_cols = [f"Volatility_pct_{window}D" for window in windows]
            result = result.with_columns(
                result.select(pl.col(vol_cols))
                .collect()
                .mean(axis=1)
                .alias("Volatility_mean")
            ).lazy()

        else:
            k = 0.34 / (1.34 + (window + 1) / (window - 1))
            price_data = self._yang_zhang_engine(
                price_data=price_data,
                window=window,
                trading_periods=trading_periods,
            )

            result = price_data.with_columns(
                (
                    (
                        pl.col("open_vol")
                        + k * pl.col("close_vol")
                        + (1 - k) * pl.col("window_rs")
                    ).sqrt()
                    * np.sqrt(trading_periods)
                    * 100
                ).alias("Volatility_pct")
            ).select(
                pl.exclude(
                    [
                        "log_ho",
                        "log_lo",
                        "log_co",
                        "log_oc",
                        "log_cc",
                        "log_oc_sq",
                        "log_cc_sq",
                        "rs",
                        "close_vol",
                        "open_vol",
                        "window_rs",
                    ]
                )
            )

        if clean:
            return result.drop_nulls()
        else:
            return result

    def _yang_zhang_engine(self, price_data, window, trading_periods):
        out = price_data.with_columns(
            [
                (
                    pl.col("log_cc_sq").rolling_sum(
                        window_size=window, min_periods=1
                    )
                    * (1.0 / (window - 1.0))
                ).alias("close_vol"),
                (
                    pl.col("log_oc_sq").rolling_sum(
                        window_size=window, min_periods=1
                    )
                    * (1.0 / (window - 1.0))
                ).alias("open_vol"),
                (
                    pl.col("rs").rolling_sum(window_size=window, min_periods=1)
                    * (1.0 / (window - 1.0))
                ).alias("window_rs"),
            ]
        )
        return out

    def _squared_returns(
        self, price_data, window=30, trading_periods=252, clean=True
    ):
        """
        Calculate squared returns over a rolling window.

        Parameters:
        ------------
        - price_data: DataFrame containing the price data
        - window: the size of the rolling window
        - trading_periods: number of trading periods in a year, default is 252
        (the common number of trading days in a year)
        - clean: Boolean indicating whether to drop NA values in the result

        Returns:
        ------------
        - DataFrame of the rolling squared returns.
        """
        # Calculate returns
        # price_data = price_data.with_columns(
        #     (pl.col("adj_close").pct_change() * 100).alias("Returns_pct"),
        # )

        # price_data = price_data.with_columns(
        #     (pl.col("Returns_pct") ** 2).alias("squared_log_returns"),
        # )

        price_data = dth.log_returns(df=price_data).with_columns(
            ((pl.col("log_returns") * 100) ** 2).alias(
                "squared_log_returns_pct"
            )
        )

        # RV_MEAN - lazyAPI execution
        if self.rv_mean is True:
            results = []
            windows = [10, 20, 30]
            for window in windows:
                result = price_data.with_columns(
                    pl.col("squared_log_returns_pct")
                    .rolling_mean(window_size=window, min_periods=1)
                    .alias(f"Volatility_pct_{window}D")
                ).select(pl.exclude(["squared_log_returns_pct"]))

                results.append(result)

            # Combine results into a single lazyFrame
            result = pl.concat(results, how="align")
            vol_cols = [f"Volatility_pct_{window}D" for window in windows]
            result = result.with_columns(
                result.select(pl.col(vol_cols))
                .collect()
                .mean(axis=1)
                .alias("Volatility_mean")
            ).lazy()

        else:
            # Calculate rolling squared returns
            result = price_data.with_columns(
                pl.col("squared_log_returns_pct")
                .rolling_mean(window_size=window, min_periods=1)
                .alias("Volatility_pct")
            ).select(pl.exclude(["squared_log_returns_pct"]))

        if clean:
            return result.drop_nulls()
        return result

    def _orats_hv(
        self, price_data, window=None, trading_periods=None, clean=True
    ):
        """
        Collect historical volatility from ORATS data API
        """
        orats = OratsData(silent=self.silent)

        result = orats.get_data(
            ticker=self.ticker,
            endpoint="historicalVolatility",
            fields=[
                "ticker",
                "tradeDate",  # renamed to `date` in OratsData()._get_data()
                "clsHv10d",
                "clsHv20d",
                "clsHv30d",
                "orHv10d",
                "orHv20d",
                "orHv30d",
            ],
            fromdate=self.fromdate,
            todate=self.todate,
        )

        # RV_MEAN - lazyAPI execution
        vol_cols = ["clsHv10d", "clsHv20d", "clsHv30d"]

        result = result.with_columns(
            result.select(pl.col(vol_cols))
            .collect()
            .mean(axis=1)
            .alias("Volatility_mean")
        )
        if clean:
            return result.drop_nulls()
        else:
            return result
