# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: plateform/request/OptStockAddRequest.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='plateform/request/OptStockAddRequest.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n6com.huasheng.quant.open.sdk.protobuf.plateform.requestB\027OptStockAddRequestProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n*plateform/request/OptStockAddRequest.proto\"?\n\x12OptStockAddRequest\x12\x0f\n\x07groupId\x18\x01 \x01(\t\x12\x18\n\x10securityCodeList\x18\x02 \x03(\tBQ\n6com.huasheng.quant.open.sdk.protobuf.plateform.requestB\x17OptStockAddRequestProtob\x06proto3'
)




_OPTSTOCKADDREQUEST = _descriptor.Descriptor(
  name='OptStockAddRequest',
  full_name='OptStockAddRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='groupId', full_name='OptStockAddRequest.groupId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='securityCodeList', full_name='OptStockAddRequest.securityCodeList', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=46,
  serialized_end=109,
)

DESCRIPTOR.message_types_by_name['OptStockAddRequest'] = _OPTSTOCKADDREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OptStockAddRequest = _reflection.GeneratedProtocolMessageType('OptStockAddRequest', (_message.Message,), {
  'DESCRIPTOR' : _OPTSTOCKADDREQUEST,
  '__module__' : 'plateform.request.OptStockAddRequest_pb2'
  # @@protoc_insertion_point(class_scope:OptStockAddRequest)
  })
_sym_db.RegisterMessage(OptStockAddRequest)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
