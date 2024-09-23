import logging
import paho.mqtt.client as mqtt
import threading
from typing import Any, Dict, cast
from mobilus_client.messages.encryptor import MessageEncryptor
from mobilus_client.messages.factory import MessageFactory
from mobilus_client.messages.status import MessageStatus
from mobilus_client.messages.validator import MessageValidator
from mobilus_client.proto import (LoginRequest, LoginResponse)
from mobilus_client.utils.types import MessageRequest


logger = logging.getLogger(__name__)


class MqttClient(mqtt.Client):
    _userdata: Dict[str, Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.authenticated_event = threading.Event()
        self.completed_event = threading.Event()
        self.enable_logger(logger)

    def send_request(self, command: str, **params: Any) -> None:
        if not self.is_connected():
            logger.error(f"Sending request - {command} failed. Client is not connected.")
            return

        message = MessageFactory.create_message(command, **params)
        status = MessageValidator.validate(message)

        if status != MessageStatus.SUCCESS:
            logger.error(f"Command - {command} returned an error - {status.name}")
            self.disconnect()
            return

        if not isinstance(message, LoginRequest):
            self._userdata['message_registry'].register_request(message)

        encrypted_message = MessageEncryptor.encrypt(
            cast(MessageRequest, message),
            self._userdata["config"].client_id,
            self._userdata['key_registry']
        )

        self.publish("module", encrypted_message)

    def on_disconnect(self, client: mqtt.Client, userdata: Any, reason_code: Any) -> None:  # type: ignore
        logger.info(f"Disconnected with result code - {reason_code}")

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: Any, reason_code: Any) -> None:  # type: ignore
        client.subscribe([
            (userdata["config"].client_id, 0),
            ("clients", 0)
        ])

    def on_subscribe(self, client: mqtt.Client, userdata: Any, mid: Any, granted_qos: Any) -> None:  # type: ignore
        self.send_request(
            "login",
            login=userdata["config"].user_login,
            password=userdata["config"].user_key
        )

    def on_message(self, client: mqtt.Client, userdata: Any, message: Any) -> None:  # type: ignore
        logger.info(f"Received message on topic - {message.topic}")

        message = MessageEncryptor.decrypt(message.payload, userdata["key_registry"])
        logger.info(f"Decrypted message - {type(message).__name__}")

        status = MessageValidator.validate(message)

        if status != MessageStatus.SUCCESS:
            logger.error(f"Message - {type(message).__name__} returned an error - {status.name}")
            self.disconnect()
            return

        logger.info(f"Message - {type(message).__name__} validated successfully")

        if isinstance(message, LoginResponse):
            userdata["key_registry"].register_keys(message)
            self.authenticated_event.set()
        else:
            userdata["message_registry"].register_response(message)

            if userdata["message_registry"].all_responses_received():
                self.completed_event.set()
