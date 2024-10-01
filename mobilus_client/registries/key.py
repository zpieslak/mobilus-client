from __future__ import annotations

from typing import TYPE_CHECKING

from mobilus_client.proto import CallEventsRequest, LoginResponse

if TYPE_CHECKING:
    from mobilus_client.utils.types import MessageRequest, MessageResponse


class KeyRegistry:
    def __init__(self, user_key: bytes) -> None:
        self._registry = {
            "user_key": user_key,
        }

    def get_keys(self) -> dict[str, bytes]:
        return self._registry

    def register_keys(self, message: LoginResponse) -> None:
        self._registry["private_key"] = message.private_key
        self._registry["public_key"] = message.public_key

    def get_decryption_key(self, message_klass: type[MessageResponse]) -> bytes:
        if message_klass == LoginResponse:
            return self._registry["user_key"]

        if message_klass == CallEventsRequest:
            return self._registry["public_key"]

        return self._registry["private_key"]

    def get_encryption_key(self, message_klass: type[MessageRequest]) -> bytes | None:
        if message_klass == CallEventsRequest:
            return self._registry.get("private_key")

        return None
