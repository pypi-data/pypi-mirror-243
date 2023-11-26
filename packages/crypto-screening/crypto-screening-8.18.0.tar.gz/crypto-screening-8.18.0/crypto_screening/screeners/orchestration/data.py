# data.py

from abc import ABCMeta
from typing import Self, ClassVar

from attrs import define

from represent import represent

__all__ = [
    "ServiceData"
]

@define(repr=False)
@represent
class ServiceData(metaclass=ABCMeta):
    """A class to represent service data."""

    name: str
    payload: str = None

    TYPE: ClassVar[str]
    NAME: ClassVar[str] = "name"
    PAYLOAD: ClassVar[str] = "payload"

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls(
            name=data[cls.NAME],
            payload=data[cls.PAYLOAD]
        )
    # end load

    def json(self) -> dict[str, str]:
        """
        Returns a json compatible representation of the data.

        :return: The data of the object.
        """

        return {self.NAME: self.name, self.PAYLOAD: self.payload}
    # end json
# end ServiceData