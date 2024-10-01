from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from mobilus_client.proto import (
    CallEvent,
    CallEventsRequest,
    CurrentStateRequest,
    DevicesListRequest,
    LoginRequest,
)

if TYPE_CHECKING:
    from mobilus_client.utils.types import MessageRequest


class CallEventsMessageBuilder:
    def build(self, device_id: str = "", value: str = "", event_number: str = "6") -> CallEventsRequest | None:
        if not device_id or not value:
            return None

        event = CallEvent()
        event.event_number = int(event_number)
        event.device_id = int(device_id)
        event.value = value

        request = CallEventsRequest()
        request.events.append(event)
        return request


class CurrentStateMessageBuilder:
    def build(self) -> CurrentStateRequest:
        return CurrentStateRequest()


class DevicesListMessageBuilder:
    def build(self) -> DevicesListRequest:
        return DevicesListRequest()


class LoginMessageBuilder:
    def build(self, login: str = "", password: bytes = b"") -> LoginRequest | None:
        if not login or not password:
            return None

        request = LoginRequest()
        request.login = login
        request.password = password
        return request


class MessageFactory:
    _builders: ClassVar[
      dict[str, LoginMessageBuilder | DevicesListMessageBuilder | CurrentStateMessageBuilder | CallEventsMessageBuilder]
     ] = {
        "call_events": CallEventsMessageBuilder(),
        "current_state": CurrentStateMessageBuilder(),
        "devices_list": DevicesListMessageBuilder(),
        "login": LoginMessageBuilder(),
    }

    @staticmethod
    def create_message(message_name: str, **kwargs: Any) -> MessageRequest | None: # noqa: ANN401
        builder = MessageFactory._builders.get(message_name)
        return builder.build(**kwargs) if builder else None
