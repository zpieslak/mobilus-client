from __future__ import annotations

import logging
import threading
from typing import Any, cast

import paho.mqtt.client as mqtt

from mobilus_client.messages.encryptor import MessageEncryptor
from mobilus_client.messages.factory import MessageFactory
from mobilus_client.messages.status import MessageStatus
from mobilus_client.messages.validator import MessageValidator
from mobilus_client.proto import LoginRequest, LoginResponse
from mobilus_client.utils.types import MessageRequest

logger = logging.getLogger(__name__)


class MqttClient(mqtt.Client):
    _client_id: bytes
    _userdata: dict[str, Any]

    def __init__(self, **kwargs: Any) -> None: # noqa: ANN401
        super().__init__(**kwargs)
        self.authenticated_event = threading.Event()
        self.completed_event = threading.Event()
        self.enable_logger(logger)

    def send_request(self, command: str, **params: str | bytes | int | None) -> None:
        if not self.is_connected():
            logger.error("Sending request - %s failed. Client is not connected.", command)
            return

        message = MessageFactory.create_message(command, **params)
        status = MessageValidator.validate(message)

        if status != MessageStatus.SUCCESS:
            logger.error("Command - %s returned an error - %s", command, status.name)
            self.disconnect()
            return

        if not isinstance(message, LoginRequest):
            self._userdata["message_registry"].register_request(message)

        encrypted_message = MessageEncryptor.encrypt(
            cast(MessageRequest, message),
            self._client_id.decode(),
            self._userdata["key_registry"],
        )

        self.publish("module", encrypted_message)

    def on_disconnect(self, _client: mqtt.Client, _userdata: dict[str, Any], reason_code: int) -> None:  # type: ignore[override]
        logger.info("Disconnected with result code - %s", reason_code)

    def on_connect(self, client: mqtt.Client, _userdata: dict[str, Any], *_args: Any) -> None:  # type: ignore[override] # noqa: ANN401
        client.subscribe([
            (self._client_id.decode(), 0),
            ("clients", 0),
        ])

    def on_subscribe(self, _client: mqtt.Client, userdata: dict[str, Any], *_args: Any) -> None:  # type: ignore[override]  # noqa: ANN401
        self.send_request(
            "login",
            login=userdata["config"].user_login,
            password=userdata["config"].user_key,
        )

    def on_message(self, _client: mqtt.Client, userdata: dict[str, Any], mqtt_message: mqtt.MQTTMessage) -> None:  # type: ignore[override]
        logger.info("Received message on topic - %s", mqtt_message.topic)

        message = MessageEncryptor.decrypt(mqtt_message.payload, userdata["key_registry"])
        logger.info("Decrypted message - %s", type(message).__name__)

        status = MessageValidator.validate(message)

        if status != MessageStatus.SUCCESS:
            logger.error("Message - %s returned an error - %s", type(message).__name__, status.name)
            self.disconnect()
            return

        logger.info("Message - %s validated successfully", type(message).__name__)

        if isinstance(message, LoginResponse):
            userdata["key_registry"].register_keys(message)
            self.authenticated_event.set()
        else:
            userdata["message_registry"].register_response(message)

            if userdata["message_registry"].all_responses_received():
                self.completed_event.set()
