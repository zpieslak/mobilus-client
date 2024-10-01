import secrets
from dataclasses import dataclass, field

from mobilus_client.utils.encryption import create_key


@dataclass
class Config:
    gateway_host: str
    user_login: str
    user_password: str

    auth_timeout_period: float = 30
    client_id: str = field(default_factory=lambda: secrets.token_hex(6).upper())
    gateway_port: int = 8884
    gateway_protocol: str = "websockets"
    timeout_period: float = 30
    user_key: bytes = b""

    def __post_init__(self) -> None:
        self.user_key = create_key(self.user_password)
