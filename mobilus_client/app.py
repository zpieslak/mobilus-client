import logging
import socket
from typing import Dict, List, Tuple
from mobilus_client.config import Config
from mobilus_client.messages.serializer import MessageSerializer
from mobilus_client.mqtt_client import MqttClient
from mobilus_client.registries.message import MessageRegistry
from mobilus_client.registries.key import KeyRegistry

logger = logging.getLogger(__name__)


class App:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.message_registry = MessageRegistry()
        self.key_registry = KeyRegistry(config.user_key)
        self.client = MqttClient(
            client_id=config.client_id,
            transport=config.gateway_protocol,
            userdata={
                "config": config,
                "key_registry": self.key_registry,
                "message_registry": self.message_registry,
            }
        )

    def call(self, commands: List[Tuple[str, Dict[str, str]]]) -> str:
        if not commands:
            return self._empty_response()

        try:
            # Connect to the MQTT broker and start the loop
            self.client.connect(self.config.gateway_host, self.config.gateway_port, 60)
            self.client.loop_start()

            # Wait for the client to authenticate
            self.client.authenticated_event.wait(timeout=self.config.auth_timeout_period)

            if not self.client.authenticated_event.is_set():
                logger.error("Failed to authenticate with the gateway host")
                return self._empty_response()

            # Execute the provided commands
            for command, params in commands:
                self.client.send_request(command, **params)

            # Wait for the completion event to be triggered
            self.client.completed_event.wait(timeout=self.config.timeout_period)
        except socket.gaierror:
            logger.error("Failed to connect to the gateway host")
        except TimeoutError:
            logger.error("Timeout occurred")
        finally:
            self.client.disconnect()

        # Return serialized responses from the message registry
        return MessageSerializer.serialize_list_to_json(
            self.message_registry.get_responses()
        )

    def _empty_response(self) -> str:
        return MessageSerializer.serialize_list_to_json([])
