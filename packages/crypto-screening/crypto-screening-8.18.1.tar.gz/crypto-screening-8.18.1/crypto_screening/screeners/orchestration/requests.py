# requests.py

import json
from enum import Enum
from abc import ABCMeta
from typing import Any, Self

from crypto_screening.screeners.orchestration.data import ServiceData

__all__ = [
    "RequestType",
    "ServiceRequest",
    "ControlRequest",
    "PauseRequest",
    "UnpauseRequest",
    "REQUESTS",
    "load_request",
    "UpdateRequest",
    "RunRequest",
    "StopRequest",
    "ConfigRequest"
]

class RequestType(Enum):
    """A class to represent an enum of request types."""

    STOP = "stop"
    RUN = "run"
    PAUSE = "pause"
    UNPAUSE = "unpause"
    CONFIG = "config"
    UPDATE = "update"
    DATA = "data"
# end RequestType

class ServiceRequest(ServiceData, metaclass=ABCMeta):
    """A class to represent a service request sent from the client to the server."""

    __slots__ = ()
# end ServiceRequest


class UpdateRequest(ServiceRequest, metaclass=ABCMeta):
    """A class to represent a service request sent from the client to the server."""

    __slots__ = ('config',)

    TYPE = RequestType.UNPAUSE.value

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Defines the data of the request.

        :param config: The options for the payload.
        """

        super().__init__(name=self.TYPE)

        self.config = config
    # end __init__

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls(
            config=json.loads(data[cls.PAYLOAD])
        )
    # end load

    def json(self) -> dict[str, str]:
        """
        Returns a json compatible representation of the data.

        :return: The data of the object.
        """

        return {
            self.NAME: self.name,
            self.PAYLOAD: json.dumps(self.config)
        }
    # end json
# end UpdateRequest

class ConfigRequest(ServiceRequest, metaclass=ABCMeta):
    """A class to represent a service request sent from the client to the server."""

    __slots__ = ()

    TYPE = RequestType.CONFIG.value

    def __init__(self) -> None:
        """Defines the data of the request."""

        super().__init__(name=self.TYPE, payload="")
    # end __init__

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls()
    # end load
# end ConfigRequest

class ControlRequest(ServiceRequest, metaclass=ABCMeta):
    """A class to represent a service request sent from the client to the server."""

    __slots__ = ()

    def __init__(self, name: str) -> None:
        """
        Defines the data of the request.

        :param name: The name of the request.
        """

        super().__init__(name=name, payload="")
    # end __init__

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls(name=data[cls.NAME])
    # end load
# end ControlRequest

class PauseRequest(ControlRequest):
    """A class to represent a service request sent from the client to the server."""

    __slots__ = ()

    TYPE = RequestType.PAUSE.value

    def __init__(self) -> None:
        """Defines the data of the request."""

        super().__init__(name=self.TYPE)
    # end __init__

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls()
    # end load
# end PauseRequest

class UnpauseRequest(ControlRequest):
    """A class to represent a service request sent from the client to the server."""

    __slots__ = ()

    TYPE = RequestType.UNPAUSE.value

    def __init__(self) -> None:
        """Defines the data of the request."""

        super().__init__(name=self.TYPE)
    # end __init__

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls()
    # end load
# end UnpauseRequest

class RunRequest(ControlRequest):
    """A class to represent a service request sent from the client to the server."""

    __slots__ = ()

    TYPE = RequestType.RUN.value

    def __init__(self) -> None:
        """Defines the data of the request."""

        super().__init__(name=self.TYPE)
    # end __init__

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls()
    # end load
# end RunRequest

class StopRequest(ControlRequest):
    """A class to represent a service request sent from the client to the server."""

    __slots__ = ()

    TYPE = RequestType.STOP.value

    def __init__(self) -> None:
        """Defines the data of the request."""

        super().__init__(name=self.TYPE)
    # end __init__

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls()
    # end load
# end StopRequest

REQUESTS: dict[str, type[ServiceRequest]] = {
    ConfigRequest.TYPE: ConfigRequest,
    UpdateRequest.TYPE: UpdateRequest,
    PauseRequest.TYPE: PauseRequest,
    UnpauseRequest.TYPE: UnpauseRequest,
    RunRequest.TYPE: RunRequest,
    StopRequest.TYPE: StopRequest
}

def load_request(data: dict[str, str]) -> ServiceRequest:
    """
    Loads the request to the correct request object.

    :param data: The data to load into the request.

    :return: The request object with the loaded data.
    """

    if ServiceRequest.NAME not in data:
        raise ValueError(f"Invalid request data: {data}")
    # end if

    name = data[ServiceData.NAME]

    if name not in REQUESTS:
        raise ValueError(
            f"Unknown request type: {name} with data: {data}."
        )
    # end if

    return REQUESTS[name].load(data)
# end load_request