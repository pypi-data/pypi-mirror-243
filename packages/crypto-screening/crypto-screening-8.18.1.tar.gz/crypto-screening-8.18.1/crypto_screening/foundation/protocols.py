# protocols.py

import datetime as dt
from typing import Protocol

import pandas as pd

__all__ = [
    "BaseScreenerProtocol",
    "BaseMarketScreenerProtocol",
    "DataCollectorProtocol"
]

TimeDuration = float | dt.timedelta

class DataCollectorProtocol(Protocol):
    """A class for the base data collector protocol."""

    location: str

    delay: TimeDuration | None
    cancel: TimeDuration | None
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