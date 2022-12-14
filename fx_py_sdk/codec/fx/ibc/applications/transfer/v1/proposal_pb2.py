# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fx/ibc/applications/transfer/v1/proposal.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fx_py_sdk.codec.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from fx_py_sdk.codec.fx.ibc.applications.transfer.v1 import transfer_pb2 as fx_dot_ibc_dot_applications_dot_transfer_dot_v1_dot_transfer__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='fx/ibc/applications/transfer/v1/proposal.proto',
  package='fx.ibc.applications.transfer.v1',
  syntax='proto3',
  serialized_options=b'Z=github.com/functionx/fx-dex/x/ibc/applications/transfer/types',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n.fx/ibc/applications/transfer/v1/proposal.proto\x12\x1f\x66x.ibc.applications.transfer.v1\x1a\x14gogoproto/gogo.proto\x1a.fx/ibc/applications/transfer/v1/transfer.proto\"\xc3\x01\n\x11UpdateDenomTraces\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12h\n\x0c\x64\x65nom_traces\x18\x03 \x03(\x0b\x32+.fx.ibc.applications.transfer.v1.DenomTraceB%\xaa\xdf\x1f\x06Traces\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:\"denom_traces\"\x12\x12\n\ndenom_keys\x18\x04 \x03(\t:\x0c\xe8\xa0\x1f\x00\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x42?Z=github.com/functionx/fx-dex/x/ibc/applications/transfer/typesb\x06proto3'
  ,
  dependencies=[gogoproto_dot_gogo__pb2.DESCRIPTOR,fx_dot_ibc_dot_applications_dot_transfer_dot_v1_dot_transfer__pb2.DESCRIPTOR,])




_UPDATEDENOMTRACES = _descriptor.Descriptor(
  name='UpdateDenomTraces',
  full_name='fx.ibc.applications.transfer.v1.UpdateDenomTraces',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='fx.ibc.applications.transfer.v1.UpdateDenomTraces.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='fx.ibc.applications.transfer.v1.UpdateDenomTraces.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='denom_traces', full_name='fx.ibc.applications.transfer.v1.UpdateDenomTraces.denom_traces', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\252\337\037\006Traces\310\336\037\000\362\336\037\023yaml:\"denom_traces\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='denom_keys', full_name='fx.ibc.applications.transfer.v1.UpdateDenomTraces.denom_keys', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'\350\240\037\000\210\240\037\000\230\240\037\000',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=154,
  serialized_end=349,
)

_UPDATEDENOMTRACES.fields_by_name['denom_traces'].message_type = fx_dot_ibc_dot_applications_dot_transfer_dot_v1_dot_transfer__pb2._DENOMTRACE
DESCRIPTOR.message_types_by_name['UpdateDenomTraces'] = _UPDATEDENOMTRACES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UpdateDenomTraces = _reflection.GeneratedProtocolMessageType('UpdateDenomTraces', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEDENOMTRACES,
  '__module__' : 'fx.ibc.applications.transfer.v1.proposal_pb2'
  # @@protoc_insertion_point(class_scope:fx.ibc.applications.transfer.v1.UpdateDenomTraces)
  })
_sym_db.RegisterMessage(UpdateDenomTraces)


DESCRIPTOR._options = None
_UPDATEDENOMTRACES.fields_by_name['denom_traces']._options = None
_UPDATEDENOMTRACES._options = None
# @@protoc_insertion_point(module_scope)
