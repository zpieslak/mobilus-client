import sys
import unittest
from unittest.mock import Mock, patch

from mobilus_client.messages.encryptor import MessageEncryptor
from mobilus_client.registries.key import KeyRegistry
from tests.factories import (
    CallEventsRequestFactory,
    CurrentStateRequestFactory,
    CurrentStateResponseFactory,
    DevicesListRequestFactory,
    DevicesListResponseFactory,
    LoginRequestFactory,
    LoginResponseFactory,
)
from tests.helpers import encrypt_message


class TestMessageEncryptor(unittest.TestCase):
    def setUp(self) -> None:
        self.client_id = "0123456789ABCDEF"
        self.user_key = b"test_user_key___"
        self.private_key = b"test_private_key"
        self.public_key = b"test_public_key_"
        self.login_response = LoginResponseFactory(
            private_key=self.private_key,
            public_key=self.public_key,
        )
        self.key_registry = KeyRegistry(self.user_key)
        self.key_registry.register_keys(self.login_response)

    @patch("time.time", return_value=1633036800, autospec=True)
    def test_encrypt_login_request(self, _mock_time: Mock) -> None:
        request = LoginRequestFactory(login="username", password=self.user_key)

        result = MessageEncryptor.encrypt(request, self.client_id, self.key_registry)

        self.assertEqual(
            result,
            b"\x00\x00\x00\r\x01aV*\x00\x01#Eg\x89\xab\xcd\xef\x04\x00\n\x08username\x12\x10test_user_key___",
        )

    @patch("time.time", return_value=1633036800, autospec=True)
    def test_encrypt_devices_list_request(self, _mock_time: Mock) -> None:
        request = DevicesListRequestFactory()

        result = MessageEncryptor.encrypt(request, self.client_id, self.key_registry)

        self.assertEqual(
            result,
            b"\x00\x00\x00\r\x03aV*\x00\x01#Eg\x89\xab\xcd\xef\x04\x00",
        )

    @patch("time.time", return_value=1633036800, autospec=True)
    def test_encrypt_current_state_request(self, _mock_time: Mock) -> None:
        request = CurrentStateRequestFactory()

        result = MessageEncryptor.encrypt(request, self.client_id, self.key_registry)

        self.assertEqual(
            result,
            b"\x00\x00\x00\r\x1aaV*\x00\x01#Eg\x89\xab\xcd\xef\x04\x00",
        )

    @patch("time.time", return_value=1633036800, autospec=True)
    def test_encrypt_call_events_request(self, _mock_time: Mock) -> None:
        request = CallEventsRequestFactory(
            event={
                "device_id": 1,
                "event_number": 1,
                "value": "value",
                "platform": 1,
            },
        )

        result = MessageEncryptor.encrypt(request, self.client_id, self.key_registry)

        self.assertEqual(
            result,
            b"\x00\x00\x00\r\raV*\x00\x01#Eg\x89\xab\xcd\xef\x04\x003\xc4\x06\xb4\x9f!\x1b\xfcj2\xd2_\xd9\xe0\x94",
        )

    def test_decrypt_login_response(self) -> None:
        message = LoginResponseFactory(
            login_status=0,
            private_key=b"test_private_key",
            public_key=b"test_public_key_",
            admin=True,
            serial_number="serial_number",
            user_id=1,
        )
        encrypted_message = encrypt_message(message, self.user_key)

        result = MessageEncryptor.decrypt(encrypted_message, self.key_registry)

        self.assertEqual(result, message)

    def test_decrypt_devices_list_response(self) -> None:
        message = DevicesListResponseFactory(
            devices=[
                {
                    "id": 1,
                    "name": "name",
                    "type": 1,
                    "icon": 1,
                    "inserttime": 1,
                    "favourite": True,
                },
            ],
        )
        encrypted_message = encrypt_message(message, self.private_key)

        result = MessageEncryptor.decrypt(encrypted_message, self.key_registry)

        self.assertEqual(result, message)

    def test_decrypt_current_state_response(self) -> None:
        message = CurrentStateResponseFactory(
            event={
                "device_id": 1,
                "event_number": 1,
                "value": "value",
            },
        )
        encrypted_message = encrypt_message(message, self.private_key)

        result = MessageEncryptor.decrypt(encrypted_message, self.key_registry)

        self.assertEqual(result, message)

    def test_decrypt_call_events_response(self) -> None:
        message = CallEventsRequestFactory(
            event={
                "device_id": 1,
                "event_number": 1,
                "value": "value",
                "platform": 1,
            },
        )
        encrypted_message = encrypt_message(message, self.public_key)

        result = MessageEncryptor.decrypt(encrypted_message, self.key_registry)

        self.assertEqual(result, message)

    def test_decrypt_invalid_message_with_short_message(self) -> None:
        encrypted_message = b"invalid"

        result = MessageEncryptor.decrypt(encrypted_message, self.key_registry)

        self.assertIsNone(result)

    def test_decrypt_invalid_message_with_long_message(self) -> None:
        encrypted_message = b"invalid_message__"

        result = MessageEncryptor.decrypt(encrypted_message, self.key_registry)

        self.assertIsNone(result)

    def test_decrypt_invalid_message_with_invalid_key(self) -> None:
        message = CallEventsRequestFactory()
        encrypted_message = encrypt_message(message, b"test_invalid_key")

        result = MessageEncryptor.decrypt(encrypted_message, self.key_registry)

        # Track flaky test
        sys.stdout.write(f"result:{type(result)}:")

        self.assertIsNone(result)
