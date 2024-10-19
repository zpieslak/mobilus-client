import socket
import unittest
from unittest.mock import ANY, Mock, patch

from mobilus_client.app import App
from mobilus_client.client import Client
from mobilus_client.config import Config
from mobilus_client.registries.message import MessageRegistry
from tests.factories import (
    CallEventsRequestFactory,
)


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config(
            gateway_host="host",
            user_login="login",
            user_password="password",
            timeout_period=0,
        )
        self.app = App(self.config)

    def test_init(self) -> None:
        self.assertEqual(self.app.config, self.config)

    @patch.object(Client, "connect_and_authenticate", side_effect=socket.gaierror, autospec=True)
    def test_call_with_invalid_gateway_host(self, _mock_connect: Mock) -> None:
        result = self.app.call([("call_events", {})])

        self.assertEqual(result, "[]")

    @patch.object(Client, "connect_and_authenticate", side_effect=TimeoutError, autospec=True)
    def test_call_with_timeout_gateway_host(self, _mock_connect: Mock) -> None:
        result = self.app.call([("call_events", {})])

        self.assertEqual(result, "[]")

    @patch.object(Client, "connect_and_authenticate", return_value=Mock(), autospec=True)
    def test_call_with_empty_commands(self, mock_connect: Mock) -> None:
        result = self.app.call([])

        mock_connect.assert_not_called()
        self.assertEqual(result, "[]")

    @patch.object(Client, "connect_and_authenticate", return_value=False, autospec=True)
    def test_call_with_not_authenticated(self, _mock_connect: Mock) -> None:
        result = self.app.call([("call_events", {})])

        self.assertEqual(result, "[]")

    @patch.object(Client, "connect_and_authenticate", return_value=True, autospec=True)
    @patch.object(Client, "terminate", return_value=Mock(), autospec=True)
    def test_call_with_wrong_commands(self, mock_terminate: Mock, mock_connect: Mock) -> None:
        result = self.app.call([("wrong", {})])

        mock_connect.assert_called_once()
        mock_terminate.assert_called_once()
        self.assertEqual(result, "[]")

    @patch.object(Client, "connect_and_authenticate", return_value=True, autospec=True)
    @patch.object(Client, "send_request", return_value=Mock(), autospec=True)
    @patch.object(Client, "terminate", return_value=Mock(), autospec=True)
    @patch.object(MessageRegistry, "get_responses", autospec=True)
    def test_call_with_commands(
            self, mock_get_responses: Mock, mock_terminate: Mock, mock_send_request: Mock, mock_connect: Mock) -> None:
        call_events_request = CallEventsRequestFactory(
            event={"device_id": 1, "event_number": 1, "value": "value", "platform": 1},
        )
        mock_get_responses.return_value = [call_events_request]

        result = self.app.call([("call_events", {"device_id": "1", "value": "value"})])

        mock_connect.assert_called_once()
        mock_send_request.assert_called_once_with(ANY, "call_events", device_id="1", value="value")
        mock_terminate.assert_called_once()
        self.assertEqual(result, '[{"events": [{"deviceId": "1", "eventNumber": 1, "value": "value", "platform": 1}]}]')
