import unittest

from mobilus_client.messages.factory import MessageFactory
from mobilus_client.proto import (
    CallEventsRequest,
    CurrentStateRequest,
    DevicesListRequest,
    LoginRequest,
)


class TestMessageFactory(unittest.TestCase):
    def test_build_call_events(self) -> None:
        factory = MessageFactory()

        result = factory.create_message("call_events", device_id=1, value="on")

        self.assertIsInstance(result, CallEventsRequest)

    def test_build_call_events_failed(self) -> None:
        factory = MessageFactory()

        result = factory.create_message("call_events")

        self.assertIsNone(result)

    def test_build_current_state(self) -> None:
        factory = MessageFactory()

        result = factory.create_message("current_state")

        self.assertIsInstance(result, CurrentStateRequest)

    def test_build_devices_list(self) -> None:
        factory = MessageFactory()

        result = factory.create_message("devices_list")

        self.assertIsInstance(result, DevicesListRequest)

    def test_build_login(self) -> None:
        factory = MessageFactory()

        result = factory.create_message("login", login="user", password=b"password")

        self.assertIsInstance(result, LoginRequest)

    def test_build_login_failed(self) -> None:
        factory = MessageFactory()

        result = factory.create_message("login")

        self.assertIsNone(result)

    def test_build_unknown(self) -> None:
        factory = MessageFactory()

        result = factory.create_message("unknown")

        self.assertIsNone(result)
