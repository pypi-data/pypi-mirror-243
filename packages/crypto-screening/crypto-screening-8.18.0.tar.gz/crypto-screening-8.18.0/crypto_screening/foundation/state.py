# state.py

import datetime as dt
from typing import (
    Iterable, ClassVar, TypeVar, Generic
)

from attrs import define

from represent import represent, Modifiers

from crypto_screening.foundation.protocols import (
    BaseScreenerProtocol, BaseMarketScreenerProtocol
)

__all__ = [
    "WaitingState"
]


_BS = TypeVar("_BS", BaseScreenerProtocol, BaseMarketScreenerProtocol)

@define(repr=False)
@represent
class WaitingState(Generic[_BS]):
    """A class to represent the waiting state of screener objects."""

    screeners: Iterable[_BS]
    start: dt.datetime
    end: dt.datetime
    stop: bool = False
    delay: float = 0
    count: int = 0
    canceled: bool = False
    cancel: float | dt.timedelta | dt.datetime = None

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        hidden=["screeners"], properties=["time"]
    )

    @property
    def time(self) -> dt.timedelta:
        """
        Returns the amount of waited time.

        :return: The waiting time.
        """

        return self.end - self.start
    # end time
# end WaitingState