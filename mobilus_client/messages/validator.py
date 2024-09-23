from typing import Optional, Union
from mobilus_client.messages.status import MessageStatus
from mobilus_client.proto import LoginResponse
from mobilus_client.utils.types import MessageRequest, MessageResponse


class MessageValidator():
    @staticmethod
    def validate(message: Optional[Union[MessageRequest, MessageResponse]]) -> MessageStatus:
        if message is None:
            return MessageStatus.UNKNOWN_MESSAGE

        if isinstance(message, LoginResponse) and message.login_status == 1:
            return MessageStatus.AUTHENTICATION_ERROR

        return MessageStatus.SUCCESS
