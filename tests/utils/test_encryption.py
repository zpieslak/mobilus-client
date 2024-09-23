import unittest
from hashlib import sha256
from struct import pack
from mobilus_client.utils.encryption import create_iv, create_key, decrypt_body, encrypt_body


class TestEncryption(unittest.TestCase):
    def test_create_iv(self) -> None:
        value = 123456
        expected_iv = bytearray(b'\x00' * 12) + pack('>I', value)
        result = create_iv(value)

        self.assertEqual(result, expected_iv)

    def test_create_key(self) -> None:
        value = "test_key"
        expected_key = sha256(value.encode('utf-8')).digest()
        result = create_key(value)

        self.assertEqual(result, expected_key)

    def test_encrypt_decrypt_body(self) -> None:
        key = create_key("secret_key")
        iv = create_iv(12345)
        plaintext = b"test message"

        encrypted = encrypt_body(key, iv, plaintext)
        decrypted = decrypt_body(key, iv, encrypted)

        self.assertNotEqual(encrypted, plaintext)
        self.assertEqual(decrypted, plaintext)

    def test_decrypt_with_wrong_key(self) -> None:
        correct_key = create_key("correct_key")
        wrong_key = create_key("wrong_key")
        iv = create_iv(12345)
        plaintext = b"test message"

        encrypted = encrypt_body(correct_key, iv, plaintext)
        decrypted = decrypt_body(wrong_key, iv, encrypted)

        self.assertNotEqual(decrypted, plaintext)

    def test_decrypt_with_wrong_iv(self) -> None:
        key = create_key("secret_key")
        correct_iv = create_iv(12345)
        wrong_iv = create_iv(54321)
        plaintext = b"test message"

        encrypted = encrypt_body(key, correct_iv, plaintext)
        decrypted = decrypt_body(key, wrong_iv, encrypted)

        self.assertNotEqual(decrypted, plaintext)
