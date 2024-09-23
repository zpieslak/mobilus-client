import struct
import time
from mobilus_client.messages.encryptor import MessageEncryptor
from mobilus_client.utils.encryption import create_iv, encrypt_body
from mobilus_client.utils.types import MessageResponse


def encrypt_message(message: MessageResponse, key: bytes) -> bytes:
    # Select category from message type
    category = MessageEncryptor.CLASS_TO_CATEGORY_MAP.get(type(message))

    # Serialize message to bytes
    body = message.SerializeToString()

    # Generate header fields
    timestamp = int(time.time())
    length = 13
    platform = 0
    response_code = 0
    user_id = b"1\x00\x00\x00\x00\x00"

    # Generate IV and encrypt the body
    iv = create_iv(timestamp)
    encrypted_body = encrypt_body(key, iv, body)

    return (
        struct.pack('>IBI6sBB', length, category, timestamp, user_id, platform, response_code) +
        encrypted_body
    )
