import unittest
from mobilus_client.config import Config
from mobilus_client.utils.encryption import create_key


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config(
            gateway_host="host",
            user_login="login",
            user_password="password",
        )

    def test_auth_timeout_period(self) -> None:
        self.assertEqual(self.config.auth_timeout_period, 30)

    def test_client_id(self) -> None:
        self.assertEqual(len(self.config.client_id), 12)

    def test_gateway_host(self) -> None:
        self.assertEqual(self.config.gateway_host, "host")

    def test_gateway_port(self) -> None:
        self.assertEqual(self.config.gateway_port, 8884)

    def test_gateway_protocol(self) -> None:
        self.assertEqual(self.config.gateway_protocol, "websockets")

    def test_timeout_period(self) -> None:
        self.assertEqual(self.config.timeout_period, 30)

    def test_user_key(self) -> None:
        self.assertEqual(self.config.user_key, create_key("password"))

    def test_user_login(self) -> None:
        self.assertEqual(self.config.user_login, "login")

    def test_user_password(self) -> None:
        self.assertEqual(self.config.user_password, "password")
