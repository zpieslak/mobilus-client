"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class LoginRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOGIN_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    login: builtins.str
    password: builtins.bytes
    def __init__(
        self,
        *,
        login: builtins.str | None = ...,
        password: builtins.bytes | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["login", b"login", "password", b"password"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["login", b"login", "password", b"password"]) -> None: ...

global___LoginRequest = LoginRequest