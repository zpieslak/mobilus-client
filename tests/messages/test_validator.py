import unittest

from mobilus_client.messages.status import MessageStatus
from mobilus_client.messages.validator import MessageValidator
from tests.factories import (
    CallEventsRequestFactory,
    CurrentStateRequestFactory,
    CurrentStateResponseFactory,
    DevicesListRequestFactory,
    DevicesListResponseFactory,
    LoginRequestFactory,
    LoginResponseFactory,
)


class TestMessageValidator(unittest.TestCase):
    def test_validate_none(self) -> None:
        self.assertEqual(MessageValidator.validate(None), MessageStatus.UNKNOWN_MESSAGE)

    def test_validate_login_response_failed(self) -> None:
        login_response = LoginResponseFactory(failed=True)

        result = MessageValidator.validate(login_response)

        self.assertEqual(result, MessageStatus.AUTHENTICATION_ERROR)

    def test_validate_login_response_succeeded(self) -> None:
        login_response = LoginResponseFactory()

        result = MessageValidator.validate(login_response)

        self.assertEqual(result, MessageStatus.SUCCESS)

    def test_validate_login_request(self) -> None:
        login_request = LoginRequestFactory()

        result = MessageValidator.validate(login_request)

        self.assertEqual(result, MessageStatus.SUCCESS)

    def test_validate_call_events_request_succeeded(self) -> None:
        call_events_request = CallEventsRequestFactory()

        result = MessageValidator.validate(call_events_request)

        self.assertEqual(result, MessageStatus.SUCCESS)

    def test_validate_current_state_request_succeeded(self) -> None:
        current_state_request = CurrentStateRequestFactory()

        result = MessageValidator.validate(current_state_request)

        self.assertEqual(result, MessageStatus.SUCCESS)

    def test_validate_current_state_response_succeeded(self) -> None:
        current_state_response = CurrentStateResponseFactory()

        result = MessageValidator.validate(current_state_response)

        self.assertEqual(result, MessageStatus.SUCCESS)

    def test_validate_devices_list_request_succeeded(self) -> None:
        devices_list_request = DevicesListRequestFactory()

        result = MessageValidator.validate(devices_list_request)

        self.assertEqual(result, MessageStatus.SUCCESS)

    def test_validate_devices_list_response_succeeded(self) -> None:
        devices_list_response = DevicesListResponseFactory()

        result = MessageValidator.validate(devices_list_response)

        self.assertEqual(result, MessageStatus.SUCCESS)
