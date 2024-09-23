import struct
import time
from google.protobuf.message import DecodeError
from typing import cast, Optional
from mobilus_client.registries.key import KeyRegistry
from mobilus_client.proto import (
    CallEventsRequest,
    CurrentStateRequest,
    CurrentStateResponse,
    DevicesListRequest,
    DevicesListResponse,
    LoginRequest,
    LoginResponse
)
from mobilus_client.utils.encryption import create_iv, decrypt_body, encrypt_body
from mobilus_client.utils.types import MessageRequest, MessageResponse


class MessageEncryptor:
    CATEGORY_MAP = {
        1: LoginRequest,
        2: LoginResponse,
        3: DevicesListRequest,
        4: DevicesListResponse,
        13: CallEventsRequest,
        26: CurrentStateRequest,
        27: CurrentStateResponse,
    }
    CLASS_TO_CATEGORY_MAP = {v: k for k, v in CATEGORY_MAP.items()}

    @staticmethod
    def encrypt(message: MessageRequest, client_id: str, key_registry: KeyRegistry) -> bytes:
        category = MessageEncryptor.CLASS_TO_CATEGORY_MAP.get(type(message))
        body = message.SerializeToString()
        timestamp = int(time.time())
        length = 13

        private_key = key_registry.get_encryption_key(type(message))

        if private_key is None:
            encrypted_body = body
        else:
            iv = create_iv(timestamp)
            encrypted_body = encrypt_body(private_key, iv, body)

        return (
            struct.pack('>IBI', length, category, timestamp) +
            bytes.fromhex(client_id) +
            struct.pack('>2B', 4, 0) +
            encrypted_body
        )

    @staticmethod
    def decrypt(encrypted_message: bytes, key_registry: KeyRegistry) -> Optional[MessageResponse]:
        # Define header format and calculate size
        header_format = '>IBI6sBB'
        header_size = struct.calcsize(header_format)

        # Do early return if message is too short
        if len(encrypted_message) < header_size:
            return None

        # Unpack header
        length, category, timestamp, user_id, platform, response_code = struct.unpack(
            header_format, encrypted_message[:header_size])

        # Extract encrypted body
        encrypted_body = encrypted_message[header_size:]

        # Choose proper klass
        message_klass = MessageEncryptor.CATEGORY_MAP.get(category)
        if message_klass is None:
            return None

        # Choose proper decryption key
        key = key_registry.get_decryption_key(message_klass)

        # Decrypt body
        iv = create_iv(timestamp)
        body = decrypt_body(key, iv, encrypted_body)

        try:
            message = cast(MessageResponse, message_klass())
            message.ParseFromString(body)
        except DecodeError:
            return None

        return message
