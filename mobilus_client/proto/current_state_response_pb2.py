# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: current_state_response.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'current_state_response.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1c\x63urrent_state_response.proto\"\x8b\x01\n\x11\x43urrentStateEvent\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x11\n\tdevice_id\x18\x02 \x01(\x03\x12\x14\n\x0c\x65vent_number\x18\x03 \x01(\x05\x12\r\n\x05value\x18\x04 \x01(\t\x12\x10\n\x08platform\x18\x05 \x01(\x05\x12\x0c\n\x04user\x18\x06 \x01(\x03\x12\x12\n\ninserttime\x18\x07 \x01(\x03\":\n\x14\x43urrentStateResponse\x12\"\n\x06\x65vents\x18\x01 \x03(\x0b\x32\x12.CurrentStateEvent')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'current_state_response_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CURRENTSTATEEVENT']._serialized_start=33
  _globals['_CURRENTSTATEEVENT']._serialized_end=172
  _globals['_CURRENTSTATERESPONSE']._serialized_start=174
  _globals['_CURRENTSTATERESPONSE']._serialized_end=232
# @@protoc_insertion_point(module_scope)
