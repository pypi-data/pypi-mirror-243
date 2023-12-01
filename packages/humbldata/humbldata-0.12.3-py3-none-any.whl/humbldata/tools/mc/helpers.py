"""
This is a helper file for MandelbrotChannel tools.
"""
import datetime as dt
import math
import re
from typing import Union

import polars as pl

from humbldata.core.helpers import DataFrameHelpers as dfh
from humbldata.core.models.abstract.errors import RangeFormatError
from humbldata.volatility.estimators import VolatilityEstimators


def _range_days(
    range: str | None = None,
    fromdate: str | dt.datetime | None = None,
    todate: str | dt.datetime | None = None,
) -> tuple:
    """
    This function calculates the number of days in a given range or between two
    dates.

    Parameters
    ----------
    range : str, optional
        The range to calculate the number of days for. The range should be a
        string containing a number followed by a period identifier
        ('d' for days, 'w' for weeks,'m' for months, 'q' for quarters, or 'y'
        for years). For example, '2w' represents two weeks, which is 14 days.
    fromdate : str or datetime.datetime, optional
        The start date to calculate the number of days from. If a string is
        provided, it should be in the format 'YYYY-MM-DD'.
    todate : str or datetime.datetime, optional
        The end date to calculate the number of days to. If a string is
        provided, it should be in the format 'YYYY-MM-DD'.

    Returns
    -------
    tuple
        The number of days in the given range or between the two dates.
        Returns fromdate and todate, if they are provided.

    Raises
    ------
    ValueError
        If an invalid range is provided.
    """
    if fromdate and todate:
        fromdate = (
            dt.datetime.strptime(fromdate, "%Y-%m-%d")
            if isinstance(fromdate, str)
            else fromdate
        )
        todate = (
            dt.datetime.strptime(todate, "%Y-%m-%d")
            if isinstance(todate, str)
            else todate
        )
        return ((todate - fromdate).days), fromdate, todate

    if range:
        range_periods = {"d": 1, "w": 7, "m": 30.4, "q": 91, "y": 365.25}
        for period, days in range_periods.items():
            if period in range:
                num_periods = int(range.split(period)[0])
                return num_periods * days, None, None

    raise RangeFormatError(
        "Invalid range. Please use 'd' for days, 'w' for weeks, 'm' for months, 'q' for quarters, or 'y' for years."
    )


def _range_format(range_str: str) -> str:
    """
    This function formats a range string into a standard format.
    The return value is to be passed to `_range_days()`.

    Parameters
    ----------
    range_str : str
        The range string to format. It should contain a number followed by a
        range part. The range part can be 'day', 'week', 'month', 'quarter', or
        'year'. The range part can be in singular or plural form and can be
        abbreviated. For example, '2 weeks', '2week', '2wks', '2wk', '2w' are
        all valid.

    Returns
    -------
    str
        The formatted range string. The number is followed by an abbreviation of
        the range part ('d' for day, 'w' for week, 'mo' for month, 'q' for
        quarter, 'y' for year). For example, '2 weeks' is formatted as '2w'.

    Raises
    ------
    RangeFormatError
        If an invalid range part is provided.
    """
    # Separate the number and range part
    num = "".join(filter(str.isdigit, range_str))

    # Find the first character after the number in the range string
    range_part = next((char for char in range_str if char.isalpha()), None)

    # Check if the range part is a valid abbreviation
    if range_part not in {"d", "w", "m", "y", "q"}:
        raise RangeFormatError(
            f"`{range_str}` could not be formatted; needs to include d, w, m, y, q"
        )

    # If the range part is "m", replace it with "mo" to represent "month"
    if range_part == "m":
        range_part = "mo"

    # Return the formatted range string
    return num + range_part


def dataset_start(
    range: str | None = None,
    fromdate: str | dt.datetime | None = None,
    todate: str | dt.datetime | None = None,
    return_dt: bool = False,
) -> str | dt.datetime:
    """
    This function calculates the start date of the dataset based on the range,
    fromdate, and todate. The purpose is to ensure that the total width of the
    dates encompasses an integer number of range widths. If necessary, the
    function extends the start date to accommodate an additional range width.

    Parameters
    ----------
    range : str | None, optional
        The range of the dataset. It can be 'd' for days, 'w' for weeks, 'm'
        for months, 'q' for quarters, or 'y' for years.
    fromdate : str | dt.datetime | None, optional
        The start date of the dataset.
    todate : str | dt.datetime | None, optional
        The end date of the dataset.
    return_dt : bool, optional
        If True, the function will return the start date as a datetime object.
        If False, the function will return the start date as a string.

    Returns
    -------
    str | dt.datetime
        The start date of the dataset to collect price data from.
    """
    if range is None or fromdate is None or todate is None:
        raise ValueError("Range, fromdate, and todate cannot be None.")

    try:
        range_width = _range_days(range=range)[
            0
        ]  # ignore None's in tuple from _range_days
        total_width, fromdate, todate = _range_days(
            fromdate=fromdate, todate=todate
        )
        width_needed = math.ceil(total_width / range_width) * range_width
        start_date = todate - dt.timedelta(days=width_needed)  # type: ignore
        if return_dt:
            return start_date
        else:
            return start_date.strftime("%Y-%m-%d")
    except ZeroDivisionError as d:
        raise ValueError("Range width cannot be zero.") from d
    except Exception as e:
        raise ValueError(
            "An error occurred while calculating the start date: " + str(e)
        ) from e


def log_mean(
    df: pl.DataFrame | pl.LazyFrame, window: str
) -> pl.DataFrame | pl.LazyFrame:
    """
    This function calculates the mean of 'log_returns' in a DataFrame or
    LazyFrame per window

    Parameters
    ----------
    df : pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame to calculate the rolling mean on.
    window : str
        The window to calculate the rolling mean over.

    Returns
    -------
    pl.DataFrame | pl.LazyFrame
        A DataFrame or LazyFrame with a "log_mean" & "date" column,
        which contains the mean of 'log_returns'. per window
    """
    df = df.set_sorted("date")

    return df.group_by_dynamic(
        "date", every=_range_format(window), closed="left", check_sorted=False
    ).agg([pl.col("log_returns").mean().alias("log_mean")])


def get_date_range(df: pl.DataFrame | pl.LazyFrame, index: int) -> tuple:
    """
    This function retrieves the start and end dates for a given range in a
    DataFrame or LazyFrame. This function is used in the `detrend()` function.

    Parameters
    ----------
    df : pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame to retrieve the date range from.
    index : int
        The index of the range to retrieve the dates for.

    Returns
    -------
    tuple
        A tuple containing the start and end dates for the range. The end date
        is None if the range is the last one in the DataFrame or LazyFrame.
    """
    df = dfh.from_lazy(df)
    start_date = df["date"][index]
    end_date = df["date"][index + 1] if index + 1 < df.shape[0] else None
    return start_date, end_date


def detrend(
    df: pl.DataFrame | pl.LazyFrame,
    mean_df: pl.DataFrame | pl.LazyFrame,
    sort: bool = False,
) -> pl.LazyFrame:
    """
    Detrends a DataFrame by subtracting the mean of each range.

    - Adds column `detrended_returns` to df
    - Adds column `range_n`: the nth range to df

    Parameters
    ----------
    df : pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame to detrend.
    mean_df : pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame containing the means for each range.
    sort : bool, optional
        If True, sorts both DataFrames by date before detrending.
        Default is False.

    Returns
    -------
    pl.DataFrame
        The detrended DataFrame.

    Examples
    --------
    >>> df = pl.DataFrame({
    ...     "date": pd.date_range(start="2020-01-01", end="2020-12-31"),
    ...     "log_returns": np.random.normal(size=366)
    ... })
    >>> mean_df = log_mean(df, range="1m")
    >>> detrended_df = mean_detrend(df, mean_df)
    """
    # Ensure both DataFrames are sorted by date
    if sort:
        df = df.sort("date")
        mean_df = mean_df.sort("date")

    df = dfh.from_lazy(df)
    mean_df = dfh.from_lazy(mean_df)

    # Initialize a list to store the detrended values
    # Initialize an empty DataFrame
    detrended_df = pl.DataFrame(
        {
            "date": pl.Series(
                "date", [], dtype=pl.Datetime(time_unit="us", time_zone="UTC")
            ),
            "detrended_returns": pl.Series(
                "detrended_returns", [], dtype=pl.Float64
            ),
            "range_n": pl.Series("range_n", [], dtype=pl.UInt16),
        }
    )

    # Iterate over the ranges in mean_df
    for i in range(mean_df.shape[0]):
        # Get the start and end dates for the current range
        start_date, end_date = get_date_range(mean_df, i)

        # Get the mean for the current range
        mean = mean_df["log_mean"][i]

        # Get the values in df that fall within the current range
        if end_date is not None:
            values = df.filter(
                (pl.col("date") >= start_date) & (pl.col("date") < end_date)
            ).select(pl.col("*").exclude("Adj Close"))
        else:
            values = df.filter(pl.col("date") >= start_date).select(
                pl.col("*").exclude("Adj Close")
            )

        # Create a DF with the detrended values and the corresponding dates
        new_df = pl.DataFrame(
            {
                "date": values["date"],
                "detrended_returns": values["log_returns"] - mean,
                "range_n": pl.Series([i] * values.shape[0]).cast(pl.UInt16),
            }
        )
        # Append the new DataFrame to detrended_df
        detrended_df = detrended_df.vstack(new_df)

    merged_df = df.join(detrended_df, on="date", how="left")

    return merged_df.lazy()


def cumdev(df: pl.LazyFrame, column: str = "detrended_returns") -> pl.LazyFrame:
    """
    Calculate the cumulative deviate series of a column in a DataFrame.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to process.
    column : str
        The name of the column to calculate the cumulative deviate series for.

    Returns
    -------
    pl.DataFrame
        The DataFrame with the cumulative deviate series added as a new column.
    """
    # Calculate the cumulative sum of the column

    df = df.with_columns(pl.col(column).cumsum().alias("cumdev"))

    _cumdev_check(df, column="cumdev")
    return df


def _cumdev_check(
    df: Union[pl.DataFrame, pl.LazyFrame], column: str = "cumdev"
) -> bool:
    """
    Check if the last value of a column in a DataFrame is 0.
    This function returns True if the last value is 0, otherwise it raises
    a ValueError and stops code execution.

    Parameters
    ----------
    df : Union[pl.DataFrame, pl.LazyFrame]
        The DataFrame to check.
    column : str
        The name of the column to check.

    Returns
    -------
    bool
        True if the last value of the column is 0, otherwise raises an error.

    Raises
    ------
    ValueError
        If the last value of the column is not close to 0.
    """
    from numpy import isclose

    # Get the last value of the column
    if isinstance(df, pl.DataFrame):
        value = df[column].tail(1)[0]
    else:
        value = df.collect()[column].tail(1)[0]
    # Check if the last value is 0
    if isclose(value, 0, atol=1e-6):
        return True
    else:
        raise ValueError(f"The value is not close to 0, it's {value}")


def cumdev_range(df: pl.LazyFrame, column: str = "cumdev") -> pl.LazyFrame:
    """
    Calculate the range (max - min) of a specified column in a DataFrame per range.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to calculate the range from.
    column : str, optional
        The column to calculate the range from, by default "cumsum".

    Returns
    -------
    float
        The range of the specified column.
    """
    return df.with_columns(
        [
            pl.col(column).min().over("range_n").alias("cumdev_min"),
            pl.col(column).max().over("range_n").alias("cumdev_max"),
        ]
    ).with_columns(
        (pl.col("cumdev_max") - pl.col("cumdev_min")).alias("R"),
    )


def cumdev_std(df: pl.LazyFrame, column: str = "cumdev") -> pl.LazyFrame:
    """
    Calculate the standard deviation of a specified column in a DataFrame for
    each range.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to calculate the standard deviation from.
    column : str, optional
        The column to calculate the standard deviation from, by default "cumdev".

    Returns
    -------
    pl.Series
        The series of standard deviations for the specified column.
    """
    return df.with_columns(
        [
            pl.col(column).std().over("range_n").alias("S"),
        ]
    )


def price_range(
    df: pl.LazyFrame | pl.DataFrame,
    RS: pl.Series,
    RS_mean: float,
    RS_max: float,
    RS_min: float,
    recent_price: float,
    cumdev_max: pl.DataFrame | pl.Series,
    cumdev_min: pl.DataFrame | pl.Series,
    RS_method: str = "RS",
    **kwargs,
) -> tuple[float, float]:
    """
    Calculate the price range based on the specified method.

    Parameters
    ----------
    df : Union[pl.LazyFrame, pl.DataFrame]
        The DataFrame to calculate the price range from.
    fast : bool, optional
        Whether to use the fast method, by default True.
    RS : Optional[pl.Series], optional
        The RS series, by default None.
    RS_mean : Optional[float], optional
        The mean of the RS series, by default None.
    RS_max : Optional[float], optional
        The maximum of the RS series, by default None.
    RS_min : Optional[float], optional
        The minimum of the RS series, by default None.
    recent_price : Optional[float], optional
        The recent price, by default None.
    cumdev_max : Optional[pl.DataFrame], optional
        The maximum range, by default None.
    cumdev_min : Optional[pl.DataFrame], optional
        The minimum range, by default None.
    RS_method : str, optional
        The method to calculate the RS, by default "RS".
    **kwargs
        Arbitrary keyword arguments.

    Returns
    -------
    Tuple[float, float]
        The top and bottom price.

    Raises
    ------
    ValueError
        If the RS_method is not one of 'RS', 'RS_mean', 'RS_max', 'RS_min'.
    """
    # Check if RS_method is one of the allowed values
    if RS_method not in ["RS", "RS_mean", "RS_max", "RS_min"]:
        raise ValueError(
            "RS_method must be one of 'RS', 'RS_mean', 'RS_max', 'RS_min'"
        )

    # Convert df to pl.Dataframe
    df = dfh.from_lazy(df)

    # Extract the latest detrended_returns Return Series
    rvol_factor = kwargs.get("rvol_factor", False)
    if rvol_factor:
        # Calculate STD where detrended_returns  are in the same rvol_bucket
        STD_detrended_returns = (
            df.select(pl.col("detrended_returns")).to_series().std()
        )
    else:
        # Calculate STD where detrended_returns are from the latest range
        STD_detrended_returns = (
            df.filter(pl.col("range_n") == pl.col("range_n").max())
            .select(pl.col("detrended_returns"))
            .to_series()
            .std()
        )
    # Calculate price_range using the last range's statistics
    if RS_method == "RS":
        price_range = (
            RS.tail(1)[0] * STD_detrended_returns * recent_price
        )  # noqa: F841
    elif RS_method == "RS_mean":
        price_range = (
            RS_mean * STD_detrended_returns * recent_price
        )  # noqa: F841
    elif RS_method == "RS_max":
        price_range = (
            RS_max * STD_detrended_returns * recent_price
        )  # noqa: F841
    elif RS_method == "RS_min":
        price_range = (
            RS_min * STD_detrended_returns * recent_price
        )  # noqa: F841

    # Relative Position Modifier
    top_modifier = cumdev_max.tail(1)[0] / (
        cumdev_max.tail(1)[0] - cumdev_min.tail(1)[0]
    )
    bottom_modifier = cumdev_min.tail(1)[0] / (
        cumdev_max.tail(1)[0] - cumdev_min.tail(1)[0]
    )

    top = price_range * top_modifier  # noqa: F841
    bottom = price_range * bottom_modifier  # noqa: F841

    top_price = round(recent_price + top, 4)  # noqa: F841
    bottom_price = round(recent_price + bottom, 4)  # noqa: F841

    return top_price, bottom_price


def add_rvol(
    df: pl.LazyFrame,
    **kwargs,  # rvol_method & window & rv_mean
) -> pl.LazyFrame:
    """
    Calculate the volatility factor of a given dataframe.

    Parameters
    ----------
    df : pl.LazyFrame
        The input dataframe.
    rvol_factor : bool, optional
        If True, calculate the volatility factor. Default is True.
    **kwargs
        If `rvol_factor=True`. You can pass:
        - 'rvol_method'
        - 'window'
        - `rv_mean'

    Returns
    -------
    pl.LazyFrame
        The output dataframe with the calculated volatility factor.
    """
    # Setup **kwargs Defaults
    rvol_method = kwargs.get("rvol_method", "std")
    window = kwargs.get("window", 30)
    rv_mean = kwargs.get("rv_mean", True)

    # Add tag to signal the df is formatted (date column is datetime)
    df._formatted = True  # type: ignore

    vol = VolatilityEstimators(silent=True, clean=True)
    out_df = vol.calculate_rvol(
        price_data=df,
        rvol_method=rvol_method,
        window=window,
        rv_mean=rv_mean,
    ).select(pl.exclude("^Volatility_pct_\\d+D$"))
    # Create Regex Dict for renaming
    rename_dict = {
        name: re.sub("(?i)^volatility_(mean|pct)$", "rvol", name)
        for name in out_df.columns
    }

    return out_df.rename(rename_dict)


def vol_buckets(
    df: pl.LazyFrame,
    lo_quantile: float = 0.4,
    hi_quantile: float = 0.8,
    range: str = "1m",
) -> pl.LazyFrame:
    """
    Function to bucket the volatility of a given dataframe.

    Parameters
    ----------
    df : pl.LazyFrame
        The input dataframe.
    lo_quantile : float, optional
        The lower quantile for bucketing. Default is 0.4.
    hi_quantile : float, optional
        The higher quantile for bucketing. Default is 0.8.
    range : str, optional
        The range for bucketing. Default is "1m".

    Returns
    -------
    pl.LazyFrame
        The output dataframe with the bucketed volatility.
    """
    current_vol = df.select(["rvol"]).tail(1).collect().to_series()[0]

    low_vol = df.select(["rvol"]).quantile(lo_quantile).collect().to_series()[0]
    mid_vol = df.select(["rvol"]).quantile(hi_quantile).collect().to_series()[0]

    lo_filter = pl.col("rvol") <= low_vol
    mid_filter = (pl.col("rvol") > low_vol) & (pl.col("rvol") <= mid_vol)
    hi_filter = pl.col("rvol") > mid_vol

    selected_cols = [
        "date",
        "R",
        "S",
        "cumdev_max",
        "cumdev_min",
        "detrended_returns",
        "rvol",
    ]

    lo_stats = df.select(selected_cols).filter(lo_filter)
    mid_stats = df.select(selected_cols).filter(mid_filter)
    hi_stats = df.select(selected_cols).filter(hi_filter)

    # Determine which stats to return based on the current_vol value
    if current_vol <= low_vol:
        return lo_stats
    elif current_vol <= mid_vol:
        return mid_stats
    else:
        return hi_stats
