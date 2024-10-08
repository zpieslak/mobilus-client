"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class CurrentStateEvent(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    DEVICE_ID_FIELD_NUMBER: builtins.int
    EVENT_NUMBER_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    PLATFORM_FIELD_NUMBER: builtins.int
    USER_FIELD_NUMBER: builtins.int
    INSERTTIME_FIELD_NUMBER: builtins.int
    id: builtins.int
    device_id: builtins.int
    event_number: builtins.int
    value: builtins.str
    platform: builtins.int
    user: builtins.int
    inserttime: builtins.int
    def __init__(
        self,
        *,
        id: builtins.int | None = ...,
        device_id: builtins.int | None = ...,
        event_number: builtins.int | None = ...,
        value: builtins.str | None = ...,
        platform: builtins.int | None = ...,
        user: builtins.int | None = ...,
        inserttime: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["device_id", b"device_id", "event_number", b"event_number", "id", b"id", "inserttime", b"inserttime", "platform", b"platform", "user", b"user", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["device_id", b"device_id", "event_number", b"event_number", "id", b"id", "inserttime", b"inserttime", "platform", b"platform", "user", b"user", "value", b"value"]) -> None: ...

global___CurrentStateEvent = CurrentStateEvent

@typing.final
class CurrentStateResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EVENTS_FIELD_NUMBER: builtins.int
    @property
    def events(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___CurrentStateEvent]: ...
    def __init__(
        self,
        *,
        events: collections.abc.Iterable[global___CurrentStateEvent] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["events", b"events"]) -> None: ...

global___CurrentStateResponse = CurrentStateResponse
