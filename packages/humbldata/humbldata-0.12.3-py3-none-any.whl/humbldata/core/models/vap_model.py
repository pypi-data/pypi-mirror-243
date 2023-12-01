import datetime as dt

import humblpatito as pt
import polars as pl

from humbldata.core.models.base_model import BaseModel


class VAPMergedModel(BaseModel):
    """
    A model to represent a humblpatito time-series; OHLCV & adj_close & date & premia_pct & ROC_1D_1 & premia_pctile & degross_quantile & gross_quantile & gross_fired & degross_fired
    Optimized for Polars
    """

    # Doesn't include ROC_<number>D_<number> column due to lack of multiple aliases
    # must drop the col before validating

    date: dt.date = pt.Field(dtype=pl.Date)
    ticker: str = pt.Field(dtype=pl.Utf8)
    Open: float = pt.Field(dtype=pl.Float64)
    High: float = pt.Field(dtype=pl.Float64)
    Low: float = pt.Field(dtype=pl.Float64)
    Close: float = pt.Field(dtype=pl.Float64)
    Adj_Close: float = pt.Field(dtype=pl.Float64, alias="Adj Close")
    Volume: int = pt.Field(dtype=pl.UInt64)
    premia_pct: float = pt.Field(dtype=pl.Float64)
    # ROC_1D_1: Optional[float] = pt.Field(dtype=pl.Float64)
    premia_pctile: float = pt.Field(dtype=pl.Float64)
    degross_quantile: float = pt.Field(dtype=pl.Float64)
    gross_quantile: float = pt.Field(dtype=pl.Float64)
    gross_fired: bool = pt.Field(dtype=pl.Boolean)
    degross_fired: bool = pt.Field(dtype=pl.Boolean)
