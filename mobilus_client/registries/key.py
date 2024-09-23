from typing import Dict, Optional, Type
from mobilus_client.proto import (
    CallEventsRequest,
    LoginResponse
)
from mobilus_client.utils.types import MessageRequest, MessageResponse


class KeyRegistry:
    def __init__(self, user_key: bytes) -> None:
        self._registry = {
            "user_key": user_key,
        }

    def get_keys(self) -> Dict[str, bytes]:
        return self._registry

    def register_keys(self, message: LoginResponse) -> None:
        self._registry["private_key"] = message.private_key
        self._registry["public_key"] = message.public_key

    def get_decryption_key(self, message_klass: Type[MessageResponse]) -> bytes:
        if message_klass == LoginResponse:
            return self._registry["user_key"]
        elif message_klass == CallEventsRequest:
            return self._registry["public_key"]
        else:
            return self._registry["private_key"]

    def get_encryption_key(self, message_klass: Type[MessageRequest]) -> Optional[bytes]:
        if message_klass == CallEventsRequest:
            return self._registry.get("private_key")
        return None
