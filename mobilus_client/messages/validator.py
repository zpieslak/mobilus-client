from __future__ import annotations

from typing import TYPE_CHECKING

from mobilus_client.messages.status import MessageStatus
from mobilus_client.proto import LoginResponse

if TYPE_CHECKING:
    from mobilus_client.utils.types import MessageRequest, MessageResponse


class MessageValidator:
    @staticmethod
    def validate(message: MessageRequest | MessageResponse | None) -> MessageStatus:
        if message is None:
            return MessageStatus.UNKNOWN_MESSAGE

        if isinstance(message, LoginResponse) and message.login_status == 1:
            return MessageStatus.AUTHENTICATION_ERROR

        return MessageStatus.SUCCESS
