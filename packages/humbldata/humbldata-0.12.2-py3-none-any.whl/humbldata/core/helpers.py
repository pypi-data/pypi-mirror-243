""" Utility functions for humbldata """
import datetime as dt
import functools
import inspect
import logging
from typing import List, Literal, Optional, Union

import pandas as pd
import polars as pl
from openbb import obb
from pandera.errors import SchemaError
from rich import print as prnt

from humbldata.core.env import Env
from humbldata.core.models.abstract.errors import HumblDataError
from humbldata.core.models.stocks_model import StocksBaseModel, StocksLogModel


class MessageHelpers:
    @staticmethod
    def log_message(msg: str, status: str, silent: bool = False):
        """
        Print a formatted and colorized message according to its status.

        Parameters
        ----------
        msg : str
            The message to print.
        status : str
            The status of the message ('success', 'info', 'warning', or 'error')
        silent : bool, optional
            If True, the function will not print the message. Default is False.

        Raises
        ------
        ValueError
            If the `status` argument is not one of 'success', 'info', 'warning',
            or 'error'.
        """

        if silent:
            return

        if status == "success":
            prnt(f"[green]:heavy_check_mark:[/green] {msg}")
        elif status == "info":
            prnt(f"[bold magenta]:information_source:[/bold magenta] {msg}")
        elif status == "warning":
            prnt(f"[yellow]:warning:[/yellow] {msg}")
        elif status == "error":
            prnt(f"[red]:x:[/red] {msg}")
        else:
            raise ValueError(
                f"Invalid status '{status}'. Expects: 'success', 'info',"
                f" 'warning', 'error'"
            )

    @staticmethod
    def get_rgb(color_name):
        """
        Get the RGB value of a color.

        Parameters
        ----------
        color_name : str
            The name of the color. Valid options are 'orange', 'lightblue',
            'yellow', 'green', and 'red'.

        Returns
        -------
        str
            The RGB value of the color as a string in the format 'rgb(x, x, x)'.

        Raises
        ------
        ValueError
            If the color_name is not one of the valid options.
        """
        # Define a dictionary that maps color names to their RGB values
        color_to_rgb: dict = {
            "orange": "rgb(255,155,0)",
            "lightblue": "rgb(50,170,230)",
            "yellow": "rgb(255,255,0)",
            "green": "rgb(10,200,10)",
            "red": "rgb(200,0,0)",
        }

        # Try to get the RGB value of the color, raise an error if the color
        # name is not valid
        try:
            return color_to_rgb[color_name]
        except KeyError as e:
            raise ValueError(
                "Invalid color name. Expected one of: 'orange', 'lightblue',"
                "'yellow', 'green', 'red'"
            ) from e


class DataFrameHelpers:
    @staticmethod
    def to_polars(df: pd.DataFrame) -> pl.LazyFrame:
        return pl.from_pandas(df, include_index=True).lazy()

    @staticmethod
    def cast_col(
        df: pl.LazyFrame | pl.DataFrame, col: str, to_dtype: type
    ) -> pl.LazyFrame | pl.DataFrame:
        return df.with_columns(pl.col(col).cast(to_dtype))

    @staticmethod
    def to_polars_safe(
        df, silent: bool = True, include_index=True, lazy: bool = True
    ):
        """
        Safely converts a pandas DataFrame to a Polars DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame or polars.DataFrame
            The DataFrame to convert.
        silent : bool, optional
            If True, the function will not print the conversion message.
            Default is True.
        include_index : bool, optional
            If True, the index of the pandas DataFrame will be included in the
            conversion. Default is True.
        lazy : bool, optional
            If True, the function will return a LazyFrame. Default is True.

        Returns
        -------
        polars.DataFrame or polars.LazyFrame
            The converted DataFrame.

        Raises
        ------
        ValueError
            If the input is neither a pandas DataFrame nor a Polars DataFrame.

        Examples
        --------
        >>> to_polars_safe(pd.DataFrame({"A": [1, 2], "B": [3, 4]}))
        shape: (2, 2)
        ┌─────┬─────┐
        │ A   ┆ B   │
        ├─────┼─────┤
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 3   │
        ├─────┼─────┤
        │ 2   ┆ 4   │
        └─────┴─────┘
        """
        if isinstance(df, pl.LazyFrame):
            MessageHelpers.log_message(
                "Input is already a Pola[orange1]rs[/orange1] LazyFrame,",
                "success",
                silent,
            )
            return df

        if isinstance(df, pd.DataFrame):
            MessageHelpers.log_message(
                "Converted [dodger_blue1]pandas[/dodger_blue1] DataFrame to"
                " Pola[orange1]rs[/orange1] DataFrame...",
                "success",
                silent,
            )
            if lazy is True:
                return pl.from_pandas(df, include_index=include_index).lazy()
            else:
                return pl.from_pandas(df, include_index=include_index)
        elif isinstance(df, pl.DataFrame) and lazy is True:
            MessageHelpers.log_message(
                "Input is already a Pola[orange1]rs[/orange1] DataFrame,"
                " making lazyDataframe",
                "warning",
                silent,
            )

            return df.lazy()
        elif isinstance(df, pl.DataFrame) and lazy is False:
            MessageHelpers.log_message(
                "Input is already a Pola[orange1]rs[/orange1] DataFrame,"
                " you do not want to make it lazy...",
                "warning",
                silent,
            )

        else:
            raise ValueError(
                "Input is neither a pandas DataFrame nor a Polars DataFrame"
            )

    @staticmethod
    def convert_to_datetime(df, column, datetime: bool = False) -> pl.LazyFrame:
        """
        Converts a specified column in a DataFrame | LazyFrame to datetime or
        date format. If it is converted to Datetime, it will be 'us' & 'UTC'

        Parameters
        ----------
        df : pandas.DataFrame or polars.DataFrame
            The DataFrame containing the column to convert.
        column : str
            The name of the column to convert.
        datetime : bool, optional
            If True, the function will convert the column to datetime format.
            If False, the function will convert the column to date format.
            Default is False.

        Returns
        -------
        polars.DataFrame or polars.LazyFrame
            The DataFrame with the converted column.

        Raises
        ------
        ValueError
            If the column is not of type Utf8 or Datetime.

        """
        # Setup: ---------------------------------------------------------------
        # Convert to a LazyFrame
        df = DataFrameHelpers.to_polars_safe(df)

        # MAIN LOGIC -----------------------------------------------------------
        col = df.select(pl.col(column))
        if col.dtypes[0] == pl.Utf8:
            if datetime:
                df = df.with_columns(
                    pl.col(column).str.strptime(pl.Datetime("us", "UTC"))
                )
            else:
                df = df.with_columns(
                    pl.col(column).str.strptime(pl.Date, "%Y-%m-%d")
                )
        elif col.dtypes[0] == pl.Datetime:
            if not datetime:
                df = df.with_columns(pl.col(column).cast(pl.Date))
            else:
                df = df.with_columns(
                    pl.col(column).cast(pl.Datetime("us", "UTC"))
                )

        return df

    @staticmethod
    def from_lazy(df: pl.DataFrame | pl.LazyFrame) -> pl.DataFrame:
        """
        Convert a LazyFrame to a DataFrame.

        Parameters
        ----------
        df : polars.LazyFrame or polars.DataFrame
            The DataFrame to convert.

        Returns
        -------
        polars.DataFrame
            The converted DataFrame.
        """
        if isinstance(df, pl.LazyFrame):
            return df.collect()
        else:
            return df


class PanderaHelpers:
    @staticmethod
    def validate_df(model):
        """
        A decorator to validate df's with `pandera`. This function only
        validates data with an argument containing 'df' in its name.
        It can accept any polars or pandas dataframe. If there is an argument
        with 'df' in the name, it converts it to a pandas DataFrame and
        validates it using the provided model. It then converts it to a Polars
        LazyFrame, converts the date column to the standard in `humbldata`
        ('us','UTC'), and updates the bound arguments with the validated df.

        Raises HumblDataError if no arguments with 'df' in the name are found.

        Parameters
        ----------
        model : pandera model
            The pandera model to validate the DataFrame against.

        Returns
        -------
        function
            The decorated function.

        Examples
        --------
        >>> @PanderaHelpers.validate_df(MyModel)
        ... def my_function(data_df, other_df):
        ...     # data_df and other_df are guaranteed to be valid pandas DataFrames here
        ...     pass
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Get the function's signature and bind the passed arguments to it
                bound_args = inspect.signature(func).bind(*args, **kwargs)
                bound_args.apply_defaults()

                # Extract arguments that contain 'df' in their name
                dfs = {
                    k: v for k, v in bound_args.arguments.items() if "df" in k
                }

                # If no DataFrame arguments are found, raise HumblDataError
                if not dfs:
                    raise HumblDataError(
                        "No arguments with 'df' in the name were found."
                    )

                # Process each DataFrame argument
                for df_name, df in dfs.items():
                    # If the input is a Polars DataFrame, convert it to a pandas DataFrame
                    if isinstance(df, pl.DataFrame):
                        df = df.to_pandas()
                    # If the input is a Polars LazyFrame, collect it into a DataFrame and then convert to pandas DataFrame
                    elif isinstance(df, pl.LazyFrame):
                        df = df.collect().to_pandas()

                    # Validate the DataFrame
                    df_validated = model.validate(df)
                    df_validated = DataFrameHelpers.to_polars_safe(df_validated)
                    # Ensures ('us','UTC') datetime
                    df_validated = DataFrameHelpers.convert_to_datetime(
                        df_validated, "date", datetime=True
                    )

                    # Update the bound arguments with the validated DataFrame
                    bound_args.arguments[df_name] = df_validated

                # Call the original function with the updated arguments
                return func(*bound_args.args, **bound_args.kwargs)

            return wrapper

        return decorator


class DataToolHelpers:
    @PanderaHelpers.validate_df(StocksLogModel)
    @staticmethod
    def log_returns(
        df: pl.DataFrame | pl.LazyFrame, column_name: str = "adj_close"
    ) -> pl.DataFrame | pl.LazyFrame:
        """
        This function calculates the log returns of a given column in a DataFrame.

        Parameters
        ----------
        df : pl.DataFrame | pl.LazyFrame
            The DataFrame or LazyFrame to calculate log returns on.
        column_name : str, optional
            The name of the column to calculate log returns on. Default is "adj_close".

        Returns
        -------
        pl.DataFrame | pl.LazyFrame
            The DataFrame or LazyFrame with a new column "log_returns" added, which contains the log returns of the specified column.
        """
        df = df.set_sorted("date")
        if "log_returns" not in df.columns:
            df = df.with_columns(
                pl.col(column_name).log().diff().alias("log_returns")
            ).drop_nulls(subset="log_returns")
        return df


class OpenBBHelpers:
    @staticmethod
    def get_recent_price(
        symbol: str | List[str],
        provider: Literal["fmp", "intrinio"] | None = None,
    ) -> float:
        """
        Get the most recent price for a given stock symbol.

        Parameters
        ----------
        symbol : str
            The stock symbol to get the price for.

        Returns
        -------
        float
            The most recent price for the stock symbol.
        """
        logging.getLogger("openbb_terminal.stocks.stocks_model").setLevel(
            logging.CRITICAL
        )

        return (
            obb.equity.price.quote(symbol, provider=provider)
            .to_df()["price"]
            .iloc[0]
        )

    @staticmethod
    def obb_login(pat: str | None = None) -> bool:
        if pat is None:
            pat = Env().OBB_PAT
        try:
            obb.account.login(pat=pat, remember_me=True)
            return True
        except Exception as e:
            raise HumblDataError(
                "An error occurred while logging into OpenBB. Details below:\n"
                + repr(e)
            ) from e
            return False

    @staticmethod
    def get_stock_prices(
        symbol: str,
        df: Union[pl.DataFrame, pd.DataFrame, None] = None,
        fromdate: str = "1950-01-01",
        todate: Optional[str] = None,
        provider: Literal[
            "alpha_vantage", "cboe", "fmp", "intrinio", "polygon", "yfinance"
        ] = "yfinance",
        silent: bool = True,
        lazy: bool = True,
        **kwargs,
    ) -> Union[pl.LazyFrame, pl.DataFrame]:
        """
        Fetches price data using openbb and formats the price data for a given
        symbol to match `StocksBaseModel` schema.

        Assigns a attribute `_formatted` to the DataFrame to indicate that the
        DataFrame has been formatted and validated by `pandera`

        Parameters
        ----------
        symbol : str
            The ticker symbol of the stock to fetch data for.
        df : Union[pd.DataFrame, pl.DataFrame, None], optional
            The price data to use. If None, the function will fetch the data.
        fromdate : str, optional
            The start date for the data fetch. Default is "1950-01-01".
        todate : Optional[str], optional
            The end date for the data fetch. If None, the function will use the current date.
        provider : Literal["alpha_vantage", "cboe", "fmp", "intrinio", "polygon", "yfinance"], optional
            The data provider to use for fetching the data. Default is "yfinance".
        silent : bool, optional
            If True, the function will NOT print messages. Default is False.
        lazy: bool, optional
            If True, the data will be converted to Polars LDF. Default is True.
        **kwargs:
            Additional parameters to pass to `obb.equity.price.historical()`.

        Returns
        -------
        Union[pl.LazyFrame, pl.DataFrame]
            The formatted price data.

        Raises
        ------
        SchemaError
            If the data cannot be validated by the `StocksBaseModel` schema.

        Examples
        --------
        >>> get_stock_prices("AAPL")
        >>> get_stock_prices("AAPL", fromdate="2020-01-01", todate="2020-12-31")
        """
        # Assign Price Data
        if df is None:
            df = (
                obb.equity.price.historical(
                    symbol=symbol,
                    start_date=str(fromdate),
                    end_date=str(todate)
                    if todate is not None
                    else str(dt.date.today()),
                    provider=provider,
                    verbose=not silent,
                    **kwargs,
                )
                .to_df()
                .reset_index()
            )
        else:
            if not isinstance(df, pd.DataFrame):
                df = DataFrameHelpers.from_lazy(df).to_pandas()

        df._formatted = True

        # Make Date Column timezone aware
        df["date"] = df["date"].dt.tz_localize("utc")

        # Rename 'adj close' column to 'adj_close' if it exists: future proofing, when yfiannce has adjusted data again which uses 'adj close'
        if "adj_close" in df.columns:
            df.rename(columns={"adj_close": "adj_close"}, inplace=True)

        # Pandera Validation
        try:
            out = None
            out = StocksBaseModel(df)
        except SchemaError as e:
            raise HumblDataError(
                """An error occurred in `get_stock_prices()` while validating 
                the data schema. Here are the details: """
                + repr(e),
            ) from e

        return pl.from_pandas(out) if not lazy else pl.from_pandas(out).lazy()
