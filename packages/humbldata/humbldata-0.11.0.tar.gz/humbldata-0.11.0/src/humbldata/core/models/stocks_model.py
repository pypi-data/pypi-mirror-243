import datetime as dt
from typing import Annotated

import pandas as pd
import pandera as pa
from pandera.typing import Float32, Float64, Series, UInt64

from humbldata.core.models.base_model import BaseModel


class StocksBaseModel(BaseModel):
    date: Series[Annotated[pd.DatetimeTZDtype, "us", "utc"]] = pa.Field(
        ge=dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc),
        le=dt.datetime.now(tz=dt.timezone.utc),
        description="The date of the recorded stock price",
        title="date",
        nullable=False,
        unique=True,
        coerce=True,
    )
    open: Series[Float64] = pa.Field(
        ge=0,
        description="Opening price on the day",
        title="Open",
        nullable=False,
        unique=False,
    )
    high: Series[Float64] = pa.Field(
        ge=0,
        description="Highest price of the day",
        title="High",
        nullable=False,
        unique=False,
    )
    low: Series[Float64] = pa.Field(
        ge=0,
        description="Lowest price of the day",
        title="Low",
        nullable=False,
        unique=False,
    )
    close: Series[Float64] = pa.Field(
        ge=0,
        description="Closing price of the day",
        title="Close",
        nullable=False,
        unique=False,
    )
    volume: Series[UInt64] = pa.Field(
        ge=0,
        description="Trade volume",
        title="Volume",
        nullable=False,
        unique=False,
        coerce=True,
    )
    adj_close: Series[float] = pa.Field(
        ge=0,
        alias="adj[_ ]close",
        regex=True,
        description="Adjusted closing price",
        title="Adj Close",
        nullable=False,
        unique=False,
    )

    class Config:
        coerce = True
        strict = "filter"
        name = "StocksBaseModel"


class StocksLogModel(BaseModel):
    """
    A pandera module used to validate a df that has the minimum columns
    needed to calculate log returns

    """

    date: Series[Annotated[pd.DatetimeTZDtype, "ns", "utc"]] = pa.Field(
        ge=dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc),
        le=dt.datetime.now(tz=dt.timezone.utc),
        description="The date of the recorded stock prices",
        title="date",
        nullable=False,
        unique=True,
        coerce=True,
    )
    adj_close: Series[float] = pa.Field(
        ge=0,
        alias="^(adj[_ ]close|close)$",
        regex=True,
        description="Adjusted closing price",
        title="Adj Close",
        nullable=False,
        unique=False,
    )

    class Config:
        coerce = True
        strict = "filter"
        name = "StocksLogModel"


class StocksLogReturnModel(StocksBaseModel):
    """
    A model to represent a stock time-series; OHLCV & adj_close & date & log_returns
    Optimized for Polars
    """

    log_returns: Series[Float64] = pa.Field(
        description="Log returns of the asset",
        title="Log Returns",
        nullable=False,
        unique=False,
    )


class StocksFullModel(StocksBaseModel):
    """
    A model to represent a stock time-series with all fields returned from
    obb.stocks.load(source="yfinance"); OHLCV & adj_close & date &
    dividends & stock_splits

    Optimized for Polars
    """

    dividends: Series[Float32] = pa.Field(
        ge=0.0,
        description="Dividends distributed for an asset",
        title="Dividends",
        nullable=False,
        unique=False,
    )
    stock_splits: Series[Float32] = pa.Field(
        description="Stock splits",
        title="Stock Splits",
        nullable=False,
        unique=False,
    )
