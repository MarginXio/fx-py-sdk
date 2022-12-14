# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trade/request/TradeEntrustRequest.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='trade/request/TradeEntrustRequest.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n2com.huasheng.quant.open.sdk.protobuf.trade.requestB\030TradeEntrustRequestProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\'trade/request/TradeEntrustRequest.proto\"\xea\x01\n\x13TradeEntrustRequest\x12\x11\n\tstockCode\x18\x01 \x01(\t\x12\x14\n\x0c\x65xchangeType\x18\x02 \x01(\t\x12\x15\n\rentrustAmount\x18\x03 \x01(\t\x12\x14\n\x0c\x65ntrustPrice\x18\x04 \x01(\t\x12\x11\n\tentrustBs\x18\x05 \x01(\t\x12\x13\n\x0b\x65ntrustType\x18\x06 \x01(\t\x12\x12\n\nclientType\x18\x07 \x01(\x05\x12\x10\n\x08\x65xchange\x18\x08 \x01(\t\x12\x13\n\x0bsessionType\x18\t \x01(\t\x12\x1a\n\x12iceBergDisplaySize\x18\n \x01(\tBN\n2com.huasheng.quant.open.sdk.protobuf.trade.requestB\x18TradeEntrustRequestProtob\x06proto3'
)




_TRADEENTRUSTREQUEST = _descriptor.Descriptor(
  name='TradeEntrustRequest',
  full_name='TradeEntrustRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='stockCode', full_name='TradeEntrustRequest.stockCode', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='exchangeType', full_name='TradeEntrustRequest.exchangeType', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustAmount', full_name='TradeEntrustRequest.entrustAmount', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustPrice', full_name='TradeEntrustRequest.entrustPrice', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustBs', full_name='TradeEntrustRequest.entrustBs', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustType', full_name='TradeEntrustRequest.entrustType', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='clientType', full_name='TradeEntrustRequest.clientType', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='exchange', full_name='TradeEntrustRequest.exchange', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sessionType', full_name='TradeEntrustRequest.sessionType', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='iceBergDisplaySize', full_name='TradeEntrustRequest.iceBergDisplaySize', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=44,
  serialized_end=278,
)

DESCRIPTOR.message_types_by_name['TradeEntrustRequest'] = _TRADEENTRUSTREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TradeEntrustRequest = _reflection.GeneratedProtocolMessageType('TradeEntrustRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRADEENTRUSTREQUEST,
  '__module__' : 'trade.request.TradeEntrustRequest_pb2'
  # @@protoc_insertion_point(class_scope:TradeEntrustRequest)
  })
_sym_db.RegisterMessage(TradeEntrustRequest)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
