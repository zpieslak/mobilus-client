from hashlib import sha256
from struct import pack

from cryptography.hazmat.decrepit.ciphers.modes import CFB
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def create_iv(value: int) -> bytes:
    return b"\x00" * 12 + pack(">I", value)


def create_key(value: str) -> bytes:
    return sha256(value.encode("utf-8")).digest()


def decrypt_body(key: bytes, iv: bytes, value: bytes) -> bytes:
    decryptor = Cipher(algorithms.AES(key), CFB(iv)).decryptor()
    return decryptor.update(value) + decryptor.finalize()


def encrypt_body(key: bytes, iv: bytes, value: bytes) -> bytes:
    encryptor = Cipher(algorithms.AES(key), CFB(iv)).encryptor()
    return encryptor.update(value) + encryptor.finalize()
