# protocols.py

import datetime as dt
from typing import Protocol

import pandas as pd

__all__ = [
    "BaseScreenerProtocol",
    "BaseMarketScreenerProtocol",
    "DataCollectorProtocol"
]

class DataCollectorProtocol(Protocol):
    """A class for the base data collector protocol."""

    location: str

    delay: float | dt.timedelta | None
    cancel: float | dt.timedelta | None
# end DataCollectorProtocol

class BaseScreenerProtocol(DataCollectorProtocol):
    """A class for the base screener protocol."""

    symbol: str
    exchange: str

    market: pd.DataFrame
# end BaseScreenerProtocol

class BaseMarketScreenerProtocol(DataCollectorProtocol):
    """A class for the base multi-screener protocol."""

    screeners: list[BaseScreenerProtocol]
# end BaseMarketScreenerProtocol