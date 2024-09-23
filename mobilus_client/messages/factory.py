from abc import ABC, abstractmethod
from typing import Any, Optional
from mobilus_client.proto import (
    CallEvent,
    CallEventsRequest,
    CurrentStateRequest,
    DevicesListRequest,
    LoginRequest,
)
from mobilus_client.utils.types import MessageRequest


class MessageBuilder(ABC):
    @abstractmethod
    def build(self, **kwargs: Any) -> Optional[MessageRequest]:
        pass


class LoginMessageBuilder(MessageBuilder):
    def build(self, **kwargs: Any) -> Optional[LoginRequest]:
        if 'login' not in kwargs or 'password' not in kwargs:
            return None

        request = LoginRequest()
        request.login = str(kwargs['login'])
        request.password = bytes(kwargs['password'])
        return request


class DevicesListMessageBuilder(MessageBuilder):
    def build(self, **kwargs: Any) -> DevicesListRequest:
        return DevicesListRequest()


class CurrentStateMessageBuilder(MessageBuilder):
    def build(self, **kwargs: Any) -> CurrentStateRequest:
        return CurrentStateRequest()


class CallEventsMessageBuilder(MessageBuilder):
    def build(self, **kwargs: Any) -> Optional[CallEventsRequest]:
        if 'device_id' not in kwargs or 'value' not in kwargs:
            return None

        event = CallEvent()
        event.event_number = int(kwargs.get('event_number', 6))
        event.device_id = int(kwargs['device_id'])
        event.value = str(kwargs['value'])

        request = CallEventsRequest()
        request.events.append(event)
        return request


class MessageFactory:
    _builders = {
        "call_events": CallEventsMessageBuilder(),
        "current_state": CurrentStateMessageBuilder(),
        "devices_list": DevicesListMessageBuilder(),
        "login": LoginMessageBuilder(),
    }

    @staticmethod
    def create_message(message_name: str, **kwargs: Any) -> Optional[MessageRequest]:
        builder = MessageFactory._builders.get(message_name)
        return builder.build(**kwargs) if builder else None
