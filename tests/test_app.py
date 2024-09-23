import socket
import unittest
from unittest.mock import Mock, patch
from mobilus_client.app import App
from mobilus_client.config import Config
from mobilus_client.mqtt_client import MqttClient
from mobilus_client.registries.message import MessageRegistry
from mobilus_client.registries.key import KeyRegistry
from tests.factories import (
    CallEventsRequestFactory,
)


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config(
            client_id="0123456789ABCDEF",
            gateway_host="host",
            user_login="login",
            user_password="password",
            timeout_period=0
        )
        self.app = App(self.config)

    def test_init(self) -> None:
        self.assertEqual(self.app.config, self.config)
        self.assertIsInstance(self.app.message_registry, MessageRegistry)
        self.assertIsInstance(self.app.key_registry, KeyRegistry)
        self.assertIsInstance(self.app.client, MqttClient)

    @patch.object(MqttClient, "connect", side_effect=socket.gaierror, autospec=True)
    def test_call_with_invalid_gateway_host(self, mock_connect: Mock) -> None:
        result = self.app.call([("call_events", {})])

        self.assertEqual(result, "[]")

    @patch.object(MqttClient, "connect", side_effect=TimeoutError, autospec=True)
    def test_call_with_timeout_gateway_host(self, mock_connect: Mock) -> None:
        result = self.app.call([("call_events", {})])

        self.assertEqual(result, "[]")

    @patch.object(MqttClient, "connect", return_value=Mock(), autospec=True)
    def test_call_with_empty_commands(self, mock_connect: Mock) -> None:
        result = self.app.call([])

        mock_connect.assert_not_called()
        self.assertEqual(result, "[]")

    @patch.object(MqttClient, "connect", return_value=Mock(), autospec=True)
    @patch.object(MqttClient, "loop_start", return_value=Mock(), autospec=True)
    def test_call_with_not_authenticated(self, mock_loop_start: Mock, mock_connect: Mock) -> None:
        self.config.auth_timeout_period = 0.0005
        result = self.app.call([("call_events", {})])

        self.assertEqual(result, "[]")

    @patch.object(MqttClient, "connect", return_value=Mock(), autospec=True)
    @patch.object(MqttClient, "loop_start", return_value=Mock(), autospec=True)
    @patch.object(MqttClient, "disconnect", return_value=Mock(), autospec=True)
    def test_call_with_wrong_commands(self, mock_disconnect: Mock, mock_loop_start: Mock, mock_connect: Mock) -> None:
        self.app.client.authenticated_event.set()
        self.app.client.completed_event.set()
        result = self.app.call([("wrong", {})])

        mock_connect.assert_called_once_with(self.app.client, "host", 8884, 60)
        mock_loop_start.assert_called_once()
        mock_disconnect.assert_called_once()
        self.assertEqual(result, "[]")

    @patch.object(MqttClient, "connect", return_value=Mock(), autospec=True)
    @patch.object(MqttClient, "loop_start", return_value=Mock(), autospec=True)
    @patch.object(MqttClient, "send_request", return_value=Mock(), autospec=True)
    @patch.object(MqttClient, "disconnect", return_value=Mock(), autospec=True)
    def test_call_with_commands(
            self, mock_disconnect: Mock, mock_send_request: Mock, mock_loop_start: Mock, mock_connect: Mock) -> None:
        self.app.client.authenticated_event.set()
        self.app.client.completed_event.set()
        call_events_request = CallEventsRequestFactory(
            event={"device_id": 1, "event_number": 1, "value": "value", "platform": 1}
        )
        self.app.message_registry.register_response(call_events_request)

        result = self.app.call([("call_events", {"device_id": "1", "value": "value"})])

        mock_connect.assert_called_once_with(self.app.client, "host", 8884, 60)
        mock_loop_start.assert_called_once()
        mock_send_request.assert_called_once_with(self.app.client, "call_events", device_id="1", value="value")
        mock_disconnect.assert_called_once()
        self.assertEqual(result, '[{"events": [{"deviceId": "1", "eventNumber": 1, "value": "value", "platform": 1}]}]')
