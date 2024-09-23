from collections import Counter
from typing import List
from mobilus_client.proto import (
    CallEventsRequest,
    CurrentStateRequest,
    CurrentStateResponse,
    DevicesListRequest,
    DevicesListResponse,
    LoginRequest,
    LoginResponse
)
from mobilus_client.utils.types import MessageRequest, MessageResponse


class MessageRegistry:
    MESSAGE_MAP = {
        CallEventsRequest: CallEventsRequest,
        CurrentStateRequest: CurrentStateResponse,
        DevicesListRequest: DevicesListResponse,
        LoginRequest: LoginResponse
    }

    def __init__(self) -> None:
        self._requests: List[MessageRequest] = []
        self._responses: List[MessageResponse] = []

    def register_request(self, message_request: MessageRequest) -> None:
        self._requests.append(message_request)

    def register_response(self, message_response: MessageResponse) -> None:
        self._responses.append(message_response)

    def get_requests(self) -> List[MessageRequest]:
        return self._requests

    def get_responses(self) -> List[MessageResponse]:
        return self._responses

    def all_responses_received(self) -> bool:
        expected_responses = Counter(self.MESSAGE_MAP[type(request)] for request in self.get_requests())
        actual_responses = Counter(type(response) for response in self.get_responses())

        return expected_responses == actual_responses
