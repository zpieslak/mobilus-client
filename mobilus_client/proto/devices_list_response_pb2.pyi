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
class Device(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    ICON_FIELD_NUMBER: builtins.int
    INSERTTIME_FIELD_NUMBER: builtins.int
    FAVOURITE_FIELD_NUMBER: builtins.int
    ASSIGNED_PLACE_IDS_FIELD_NUMBER: builtins.int
    ASSIGNED_GROUP_IDS_FIELD_NUMBER: builtins.int
    id: builtins.int
    name: builtins.str
    type: builtins.int
    icon: builtins.int
    inserttime: builtins.int
    favourite: builtins.bool
    @property
    def assigned_place_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def assigned_group_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        id: builtins.int | None = ...,
        name: builtins.str | None = ...,
        type: builtins.int | None = ...,
        icon: builtins.int | None = ...,
        inserttime: builtins.int | None = ...,
        favourite: builtins.bool | None = ...,
        assigned_place_ids: collections.abc.Iterable[builtins.int] | None = ...,
        assigned_group_ids: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["favourite", b"favourite", "icon", b"icon", "id", b"id", "inserttime", b"inserttime", "name", b"name", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["assigned_group_ids", b"assigned_group_ids", "assigned_place_ids", b"assigned_place_ids", "favourite", b"favourite", "icon", b"icon", "id", b"id", "inserttime", b"inserttime", "name", b"name", "type", b"type"]) -> None: ...

global___Device = Device

@typing.final
class DevicesListResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICES_FIELD_NUMBER: builtins.int
    @property
    def devices(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Device]: ...
    def __init__(
        self,
        *,
        devices: collections.abc.Iterable[global___Device] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["devices", b"devices"]) -> None: ...

global___DevicesListResponse = DevicesListResponse
