import random
from dataclasses import dataclass
from mobilus_client.utils.encryption import create_key


@dataclass
class Config:
    gateway_host: str
    user_login: str
    user_password: str

    auth_timeout_period: float = 30
    client_id: str = ''.join(random.choice('0123456789ABCDEF') for _ in range(12))
    gateway_port: int = 8884
    gateway_protocol: str = "websockets"
    timeout_period: float = 30
    user_key: bytes = b''

    def __post_init__(self) -> None:
        self.user_key = create_key(self.user_password)
