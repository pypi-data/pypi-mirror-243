# responses.py

import json
from enum import Enum
from abc import ABCMeta
from typing import Any, Self

from crypto_screening.screeners.orchestration.data import ServiceData
from crypto_screening.screeners.orchestration.requests import (
    ServiceRequest
)

__all__ = [
    "SuccessResponse",
    "ServiceResponse",
    "PauseSuccessResponse",
    "UnpauseSuccessResponse",
    "JSONErrorResponse",
    "ErrorResponse",
    "RESPONSES",
    "ResponseType",
    "RequestErrorResponse",
    "DataErrorResponse",
    "load_response",
    "UpdateSuccessResponse",
    "StopSuccessResponse",
    "RunSuccessResponse",
    "ConfigResponse"
]

class ServiceResponse(ServiceData, metaclass=ABCMeta):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()
# end ServiceResponse

class ResponseType(Enum):
    """A class to represent an enum of request types."""

    ERROR = "error"
    SUCCESS = "success"
    CONFIG = "config"
# end RequestType

class ConfigResponse(ServiceResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    TYPE = ResponseType.ERROR.value

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Defines the attributes of the response.

        :param config: The config data.
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

        return cls(config=json.loads(data[cls.PAYLOAD]))
    # end load

    def json(self) -> dict[str, str]:
        """
        Returns a json compatible representation of the data.

        :return: The data of the object.
        """

        return {
            self.NAME: self.name,
            self.PAYLOAD: json.dumps(self.payload)
        }
    # end json
# end ConfigResponse

class ErrorResponse(ServiceResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    TYPE = ResponseType.ERROR.value

    def __init__(self, message: str) -> None:
        """
        Defines the attributes of the response.

        :param message: The error message to send.
        """

        super().__init__(name=self.TYPE, payload=message)
    # end __init__

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls(message=data[cls.PAYLOAD])
    # end load
# end ErrorResponse

class JSONErrorResponse(ErrorResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    def __init__(self) -> None:
        """Defines the attributes of the response."""

        super().__init__(message="JSON incompatible payload")
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
# end JSONErrorResponse

class RequestErrorResponse(ErrorResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    def __init__(self) -> None:
        """Defines the attributes of the response."""

        super().__init__(message="Unknown request")
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
# end RequestErrorResponse

class DataErrorResponse(ErrorResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    def __init__(self) -> None:
        """Defines the attributes of the response."""

        super().__init__(message="Arbitrage option incompatible data")
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
# end DataErrorResponse

class SuccessResponse(ServiceResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    TYPE = ResponseType.SUCCESS.value

    def __init__(self, message: str) -> None:
        """
        Defines the attributes of the response.

        :param message: The error message to send.
        """

        super().__init__(name=self.TYPE, payload=message)
    # end __init__

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Loads the data into a new instance of the class.

        :param data: The data to load into the object.

        :return: The new instance of the class.
        """

        return cls(message=data[cls.PAYLOAD])
    # end load
# end SuccessResponse

class PauseSuccessResponse(SuccessResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    def __init__(self) -> None:
        """Defines the attributes of the response."""

        super().__init__(message="Successfully paused")
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
# end PauseSuccessResponse

class UnpauseSuccessResponse(SuccessResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    def __init__(self) -> None:
        """Defines the attributes of the response."""

        super().__init__(message="Successfully unpaused")
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
# end UnpauseSuccessResponse

class RunSuccessResponse(SuccessResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    def __init__(self) -> None:
        """Defines the attributes of the response."""

        super().__init__(message="Successfully ran")
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
# end RunSuccessResponse

class StopSuccessResponse(SuccessResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    def __init__(self) -> None:
        """Defines the attributes of the response."""

        super().__init__(message="Successfully stopped")
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
# end StopSuccessResponse

class UpdateSuccessResponse(SuccessResponse):
    """A class to represent a service response sent from the server to the client."""

    __slots__ = ()

    def __init__(self) -> None:
        """Defines the attributes of the response."""

        super().__init__(message="Successfully updated")
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
# end UpdateSuccessResponse

RESPONSES: dict[str, type[ServiceResponse]] = {
    ErrorResponse.TYPE: ErrorResponse,
    SuccessResponse.TYPE: SuccessResponse,
    RunSuccessResponse.TYPE: RunSuccessResponse,
    StopSuccessResponse.TYPE: StopSuccessResponse,
    UpdateSuccessResponse.TYPE: UpdateSuccessResponse,
    ConfigResponse.TYPE: ConfigResponse
}

def load_response(data: dict[str, str]) -> ServiceResponse:
    """
    Loads the response to the correct response object.

    :param data: The data to load into the response.

    :return: The response object with the loaded data.
    """

    if ServiceRequest.NAME not in data:
        raise ValueError(f"Invalid response data: {data}")
    # end if

    name = data[ServiceData.NAME]

    if name not in RESPONSES:
        raise ValueError(
            f"Unknown response type: {name} with data: {data}."
        )
    # end if

    return RESPONSES[name].load(data)
# end load_response