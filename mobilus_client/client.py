from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING, Any

import paho.mqtt.client as mqtt

from mobilus_client.messages.encryptor import MessageEncryptor
from mobilus_client.messages.factory import MessageFactory
from mobilus_client.messages.status import MessageStatus
from mobilus_client.messages.validator import MessageValidator
from mobilus_client.proto import LoginRequest, LoginResponse

if TYPE_CHECKING:
    from mobilus_client.config import Config
    from mobilus_client.registries.key import KeyRegistry
    from mobilus_client.registries.message import MessageRegistry

logger = logging.getLogger(__name__)


class Client:
    def __init__(
            self, client_id: str, config: Config, key_registry: KeyRegistry, message_registry: MessageRegistry) -> None:
        self.config = config
        self.client_id = client_id
        self.shared_topic = "clients"
        self.command_topic = "module"
        self.key_registry = key_registry
        self.message_registry = message_registry
        self.authenticated_event = threading.Event()
        self.completed_event = threading.Event()

        self.mqtt_client = mqtt.Client(client_id=self.client_id, transport=config.gateway_protocol)
        self._configure_client()

    def connect_and_authenticate(self) -> bool:
        self.mqtt_client.connect(self.config.gateway_host, self.config.gateway_port)
        self.mqtt_client.loop_start()

        # Wait for the client to authenticate
        self.authenticated_event.wait(timeout=self.config.auth_timeout_period)

        if not self.authenticated_event.is_set():
            logger.error("Failed to authenticate with the gateway host")
            return False

        return True

    def send_request(self, command: str, **params: str | bytes | int | None) -> None:
        if not self.mqtt_client.is_connected():
            logger.error("Sending request - %s failed. Client is not connected.", command)
            return

        message = MessageFactory.create_message(command, **params)
        status = MessageValidator.validate(message)

        if status != MessageStatus.SUCCESS or message is None:
            logger.error("Command - %s returned an error - %s", command, status.name)
            self.terminate()
            return

        if not isinstance(message, LoginRequest):
            self.message_registry.register_request(message)

        encrypted_message = MessageEncryptor.encrypt(
            message,
            self.client_id,
            self.key_registry,
        )

        self.mqtt_client.publish(self.command_topic, encrypted_message)

    def terminate(self) -> None:
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def on_disconnect_callback(self, _client: mqtt.Client, _userdata: None, reason_code: int) -> None:
        logger.info("Disconnected with result code - %s", reason_code)

    def on_connect_callback(
            self, _client: mqtt.Client, _userdata: None, _flags: dict[str, Any], _reason_code: int) -> None:
        self.mqtt_client.subscribe([
            (self.client_id, 0),
            (self.shared_topic, 0),
        ])

    def on_subscribe_callback(self, _client: mqtt.Client, _userdata: None, _mid: int, _granted_qos: tuple[int]) -> None:
        self.send_request(
            "login",
            login=self.config.user_login,
            password=self.config.user_key,
        )

    def on_message_callback(self, _client: mqtt.Client, _userdata: None, mqtt_message: mqtt.MQTTMessage) -> None:
        logger.info("Received message on topic - %s", mqtt_message.topic)

        message = MessageEncryptor.decrypt(mqtt_message.payload, self.key_registry)
        logger.info("Decrypted message - %s", type(message).__name__)

        if message is None:
            logger.info("Failed to decrypt message, ignoring")
            return

        status = MessageValidator.validate(message)

        if status != MessageStatus.SUCCESS:
            logger.error("Message - %s returned an error - %s", type(message).__name__, status.name)
            self.terminate()
            return

        logger.info("Message - %s validated successfully", type(message).__name__)

        if isinstance(message, LoginResponse):
            self.key_registry.register_keys(message)
            self.authenticated_event.set()
        elif self.message_registry.is_expected_response(message):
            self.message_registry.register_response(message)

            if self.message_registry.all_responses_received():
                self.completed_event.set()

    def _configure_client(self) -> None:
        self.mqtt_client.enable_logger(logger)
        self.mqtt_client.on_connect = self.on_connect_callback
        self.mqtt_client.on_disconnect = self.on_disconnect_callback
        self.mqtt_client.on_subscribe = self.on_subscribe_callback
        self.mqtt_client.on_message = self.on_message_callback
