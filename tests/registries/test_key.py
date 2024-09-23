import unittest
from mobilus_client.registries.key import KeyRegistry
from tests.factories import (
    LoginResponseFactory,
)
from mobilus_client.proto import (
    CallEventsRequest,
    CurrentStateRequest,
    CurrentStateResponse,
    DevicesListRequest,
    DevicesListResponse,
    LoginResponse,
    LoginRequest,
)


class TestKeyRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.user_key = b"test_key"
        self.registry = KeyRegistry(self.user_key)
        self.login_response = LoginResponseFactory(
            private_key=b"test_private_key",
            public_key=b"test_public_key"
        )
        self.registry.register_keys(self.login_response)

    def test_get_decryption_key_for_login_response(self) -> None:
        result = self.registry.get_decryption_key(LoginResponse)

        self.assertEqual(result, self.user_key)

    def test_get_decryption_key_for_call_events_request(self) -> None:
        result = self.registry.get_decryption_key(CallEventsRequest)

        self.assertEqual(result, self.login_response.public_key)

    def test_get_decryption_key_for_devices_list_response(self) -> None:
        result = self.registry.get_decryption_key(DevicesListResponse)

        self.assertEqual(result, self.login_response.private_key)

    def test_get_decryption_key_for_current_state_response(self) -> None:
        result = self.registry.get_decryption_key(CurrentStateResponse)

        self.assertEqual(result, self.login_response.private_key)

    def test_get_encryption_key_for_call_events_request(self) -> None:
        result = self.registry.get_encryption_key(CallEventsRequest)

        self.assertEqual(result, self.login_response.private_key)

    def test_get_encryption_key_for_devices_list_request(self) -> None:
        result = self.registry.get_encryption_key(DevicesListRequest)

        self.assertIsNone(result)

    def test_get_encryption_key_for_current_state_request(self) -> None:
        result = self.registry.get_encryption_key(CurrentStateRequest)

        self.assertIsNone(result)

    def test_get_encryption_key_for_login_request(self) -> None:
        result = self.registry.get_encryption_key(LoginRequest)

        self.assertIsNone(result)
