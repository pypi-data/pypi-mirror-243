import datetime as dt

import humblpatito as pt
import polars as pl

from humbldata.core.models.base_model import BaseModel


class MCModel(BaseModel):
    date: dt.date = pt.Field(
        dtype=pl.Date,
        unique=True,
        title="date",
        description="Date of the Mandelbrot Channel calculation",
    )
    symbol: str = pt.Field(
        dtype=pl.Utf8,
        title="symbol",
        description="Ticker of the Mandelbrot Channel",
    )
    mc_low: float = pt.Field(
        dtype=pl.Float64,
        title="mc_low",
        description="Bottom Boundary of Mandelbrot Channel",
    )
    adj_close: float = pt.Field(
        dtype=pl.Float64,
        title="adj_close",
        description="Adjusted closing price of the stock",
    )
    mc_hi: float = pt.Field(
        dtype=pl.Float64,
        title="mc_hi",
        description="Top Boundary of Mandelbrot Channel",
    )
