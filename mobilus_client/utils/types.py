from typing import Union
from mobilus_client.proto import (
    CallEventsRequest,
    CurrentStateRequest,
    CurrentStateResponse,
    DevicesListRequest,
    DevicesListResponse,
    LoginRequest,
    LoginResponse
)

MessageRequest = Union[
    CallEventsRequest,
    CurrentStateRequest,
    DevicesListRequest,
    LoginRequest
]
MessageResponse = Union[
    CallEventsRequest,
    CurrentStateResponse,
    DevicesListResponse,
    LoginResponse
]
