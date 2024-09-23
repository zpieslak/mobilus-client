from enum import Enum


class MessageStatus(Enum):
    SUCCESS = 0
    AUTHENTICATION_ERROR = 1
    UNKNOWN_MESSAGE = 2
