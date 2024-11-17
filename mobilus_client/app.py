import logging
import secrets
import socket

from mobilus_client.client import Client
from mobilus_client.config import Config
from mobilus_client.messages.serializer import MessageSerializer
from mobilus_client.registries.key import KeyRegistry
from mobilus_client.registries.message import MessageRegistry

logger = logging.getLogger(__name__)


class App:
    def __init__(self, config: Config) -> None:
        self.config = config

    def call(self, commands: list[tuple[str, dict[str, str]]]) -> str:
        if not commands:
            return self._empty_response()

        # Initialize client and registries
        key_registry = KeyRegistry(self.config.user_key)
        message_registry = MessageRegistry()

        client = Client(
            client_id=secrets.token_hex(6).upper(),
            config=self.config,
            key_registry=key_registry,
            message_registry=message_registry,
        )

        try:
            # Connect to the MQTT broker and authenticate
            if not client.connect_and_authenticate():
                return self._empty_response()

            # Execute the provided commands
            for command, params in commands:
                client.send_request(command, **params)

            # Wait for the completion event to be triggered
            client.completed_event.wait(timeout=self.config.timeout_period)
        except socket.gaierror:
            logger.error("Failed to connect to the gateway host")
        except TimeoutError:
            logger.error("Timeout occurred")
        finally:
            client.terminate()

        # Return serialized responses from the message registry
        return MessageSerializer.serialize_list_to_json(
            message_registry.get_responses(),
        )

    def _empty_response(self) -> str:
        return MessageSerializer.serialize_list_to_json([])
