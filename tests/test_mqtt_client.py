import threading
import unittest
from unittest.mock import ANY, Mock, patch

from mobilus_client.config import Config
from mobilus_client.mqtt_client import MqttClient
from mobilus_client.proto import (
    CallEventsRequest,
    CurrentStateRequest,
    DevicesListRequest,
)
from mobilus_client.registries.key import KeyRegistry
from mobilus_client.registries.message import MessageRegistry
from tests.factories import (
    CallEventsRequestFactory,
    CurrentStateResponseFactory,
    DevicesListResponseFactory,
    LoginResponseFactory,
)
from tests.helpers import encrypt_message


class TestMQTTClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client_id = "0123456789ABCDEF"
        self.config = Config(
            gateway_host="host",
            user_login="login",
            user_password="password",
            timeout_period=0,
        )

        self.message_registry = MessageRegistry()
        self.key_registry = KeyRegistry(self.config.user_key)
        self.client = MqttClient(
            client_id=self.client_id,
            transport=self.config.gateway_protocol,
            userdata={
                "config": self.config,
                "key_registry": self.key_registry,
                "message_registry": self.message_registry,
            },
        )

    def test_init(self) -> None:
        self.client = MqttClient()

        self.assertIsInstance(self.client, MqttClient)
        self.assertIsInstance(self.client.authenticated_event, threading.Event)
        self.assertIsInstance(self.client.completed_event, threading.Event)

    @patch.object(MqttClient, "is_connected", return_value=False, autospec=True)
    @patch.object(MqttClient, "publish", return_value=Mock(), autospec=True)
    def test_send_request_when_not_connected(self, mock_publish: Mock, _mock_is_connected: Mock) -> None:
        self.client.send_request("login", login="user", password=self.config.user_key)

        mock_publish.assert_not_called()

    @patch.object(MqttClient, "is_connected", return_value=True, autospec=True)
    @patch.object(MqttClient, "disconnect", return_value=Mock(), autospec=True)
    @patch.object(MqttClient, "publish", return_value=Mock(), autospec=True)
    def test_send_request_with_wrong_command(
            self, mock_publish: Mock, mock_disconnect: Mock, _mock_is_connected: Mock) -> None:
        self.client.send_request("fake")

        mock_disconnect.assert_called_once()
        mock_publish.assert_not_called()

    @patch("time.time", return_value=1633036800)
    @patch.object(MqttClient, "is_connected", return_value=True, autospec=True)
    @patch.object(MqttClient, "publish", return_value=Mock(), autospec=True)
    def test_send_request_with_login_request(
            self, mock_publish: Mock, _mock_is_connected: Mock, _mock_time: Mock) -> None:
        self.client.send_request("login", login="user", password=self.config.user_key)

        self.assertEqual(self.message_registry.get_requests(), [])
        mock_publish.assert_called_once_with(
            self.client,
            "module",
            (
                b"\x00\x00\x00\r\x01aV*\x00\x01#Eg\x89\xab\xcd\xef\x04\x00\n\x04user\x12 "
                b"^\x88H\x98\xda(\x04qQ\xd0\xe5o\x8d\xc6)'s`=\rj\xab\xbd\xd6*\x11\xefr\x1d\x15B\xd8"
            ),
        )

    @patch("time.time", return_value=1633036800)
    @patch.object(MqttClient, "is_connected", return_value=True, autospec=True)
    @patch.object(MqttClient, "publish", return_value=Mock(), autospec=True)
    def test_send_request_with_call_events_request(
            self, mock_publish: Mock, _mock_is_connected: Mock, _mock_time: Mock) -> None:
        login_response = LoginResponseFactory(private_key=b"test_private_key")
        self.key_registry.register_keys(login_response)

        self.client.send_request("call_events", device_id="0", value="value")

        self.assertIsInstance(self.message_registry.get_requests()[0], CallEventsRequest)
        mock_publish.assert_called_once_with(
            self.client,
            "module",
            b"\x00\x00\x00\r\raV*\x00\x01#Eg\x89\xab\xcd\xef\x04\x003\xc2\x06\xb5\x9f&\x1b\xfcj2\xd2_\xd9",
        )

    @patch("time.time", return_value=1633036800)
    @patch.object(MqttClient, "is_connected", return_value=True, autospec=True)
    @patch.object(MqttClient, "publish", return_value=Mock(), autospec=True)
    def test_send_request_with_current_state_request(
            self, mock_publish: Mock, _mock_is_connected: Mock, _mock_time: Mock) -> None:
        login_response = LoginResponseFactory(private_key=b"test_private_key")
        self.key_registry.register_keys(login_response)

        self.client.send_request("current_state")

        self.assertIsInstance(self.message_registry.get_requests()[0], CurrentStateRequest)
        mock_publish.assert_called_once_with(
            self.client,
            "module",
            b"\x00\x00\x00\r\x1aaV*\x00\x01#Eg\x89\xab\xcd\xef\x04\x00",
        )

    @patch("time.time", return_value=1633036800)
    @patch.object(MqttClient, "is_connected", return_value=True, autospec=True)
    @patch.object(MqttClient, "publish", return_value=Mock(), autospec=True)
    def test_send_request_with_devices_list_request(
            self, mock_publish: Mock, _mock_is_connected: Mock, _mock_time: Mock) -> None:
        login_response = LoginResponseFactory(private_key=b"test_private_key")
        self.key_registry.register_keys(login_response)

        self.client.send_request("devices_list")

        self.assertIsInstance(self.message_registry.get_requests()[0], DevicesListRequest)
        mock_publish.assert_called_once_with(
            self.client,
            "module",
            b"\x00\x00\x00\r\x03aV*\x00\x01#Eg\x89\xab\xcd\xef\x04\x00",
        )

    @patch("logging.Logger.info", return_value=Mock(), autospec=True)
    def test_on_disconnect(self, mock_info: Mock) -> None:
        self.client.on_disconnect(Mock(), {}, 0)

        mock_info.assert_called_once_with(ANY, "Disconnected with result code - %s", 0)

    @patch.object(MqttClient, "subscribe", return_value=Mock(), autospec=True)
    def test_on_connect(self, mock_subscribe: Mock) -> None:
        self.client.on_connect(self.client, {"config": self.config}, None, 0)

        mock_subscribe.assert_called_once_with(
            self.client,
            [
                (self.client_id, 0),
                ("clients", 0),
            ],
        )

    @patch.object(MqttClient, "send_request", return_value=Mock(), autospec=True)
    def test_on_subscribe(self, mock_send_request: Mock) -> None:
        self.client.on_subscribe(self.client, {"config": self.config}, 0, None)

        mock_send_request.assert_called_once_with(
            self.client, "login", login=self.config.user_login, password=self.config.user_key)

    @patch.object(MqttClient, "disconnect", return_value=Mock(), autospec=True)
    def test_on_message_invalid(self, mock_disconnect: Mock) -> None:
        message = Mock(payload=b"invalid")

        self.client.on_message(self.client, {"config": self.config, "key_registry": self.key_registry}, message)

        mock_disconnect.assert_called_once()

    def test_on_message_login_response(self) -> None:
        login_response = LoginResponseFactory()
        encrypted_message = encrypt_message(login_response, self.config.user_key)
        message = Mock(payload=encrypted_message)

        self.client.on_message(self.client, {"config": self.config, "key_registry": self.key_registry}, message)

        self.assertTrue(self.client.authenticated_event.is_set())
        self.assertEqual(self.key_registry.get_keys(), {
            "user_key": self.config.user_key,
            "private_key": login_response.private_key,
            "public_key": login_response.public_key,
        })

    def test_on_message_call_events_request_all_completed(self) -> None:
        login_response = LoginResponseFactory(public_key=b"test_public_key_")
        self.key_registry.register_keys(login_response)

        call_events_request = CallEventsRequestFactory()
        self.message_registry.register_request(CallEventsRequest())
        encrypted_message = encrypt_message(call_events_request, login_response.public_key)
        message = Mock(payload=encrypted_message)

        self.client.on_message(
            self.client, {
                "config": self.config,
                "key_registry": self.key_registry,
                "message_registry": self.message_registry,
            }, message)
        self.assertEqual(self.message_registry.get_responses(), [call_events_request])
        self.assertTrue(self.client.completed_event.is_set())

    def test_on_message_current_state_response_not_all_completed(self) -> None:
        login_response = LoginResponseFactory(private_key=b"test_private_key")
        self.key_registry.register_keys(login_response)

        current_state_response = CurrentStateResponseFactory()
        encrypted_message = encrypt_message(current_state_response, login_response.private_key)
        message = Mock(payload=encrypted_message)

        self.client.on_message(
            self.client, {
                "config": self.config,
                "key_registry": self.key_registry,
                "message_registry": self.message_registry,
            }, message)
        self.assertEqual(self.message_registry.get_responses(), [current_state_response])
        self.assertFalse(self.client.completed_event.is_set())

    def test_on_message_devices_list_response_not_all_completed(self) -> None:
        login_response = LoginResponseFactory(private_key=b"test_private_key")
        self.key_registry.register_keys(login_response)

        devices_list_response = DevicesListResponseFactory()
        encrypted_message = encrypt_message(devices_list_response, login_response.private_key)
        message = Mock(payload=encrypted_message)

        self.client.on_message(
            self.client, {
                "config": self.config,
                "key_registry": self.key_registry,
                "message_registry": self.message_registry,
            }, message)
        self.assertEqual(self.message_registry.get_responses(), [devices_list_response])
        self.assertFalse(self.client.completed_event.is_set())
