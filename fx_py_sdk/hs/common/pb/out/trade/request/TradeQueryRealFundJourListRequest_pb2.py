# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trade/request/TradeQueryRealFundJourListRequest.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='trade/request/TradeQueryRealFundJourListRequest.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n2com.huasheng.quant.open.sdk.protobuf.trade.requestB&TradeQueryRealFundJourListRequestProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n5trade/request/TradeQueryRealFundJourListRequest.proto\"d\n!TradeQueryRealFundJourListRequest\x12\x14\n\x0c\x65xchangeType\x18\x01 \x01(\t\x12\x15\n\rqueryParamStr\x18\x02 \x01(\t\x12\x12\n\nqueryCount\x18\x03 \x01(\x05\x42\\\n2com.huasheng.quant.open.sdk.protobuf.trade.requestB&TradeQueryRealFundJourListRequestProtob\x06proto3'
)




_TRADEQUERYREALFUNDJOURLISTREQUEST = _descriptor.Descriptor(
  name='TradeQueryRealFundJourListRequest',
  full_name='TradeQueryRealFundJourListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='exchangeType', full_name='TradeQueryRealFundJourListRequest.exchangeType', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queryParamStr', full_name='TradeQueryRealFundJourListRequest.queryParamStr', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queryCount', full_name='TradeQueryRealFundJourListRequest.queryCount', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=57,
  serialized_end=157,
)

DESCRIPTOR.message_types_by_name['TradeQueryRealFundJourListRequest'] = _TRADEQUERYREALFUNDJOURLISTREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TradeQueryRealFundJourListRequest = _reflection.GeneratedProtocolMessageType('TradeQueryRealFundJourListRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRADEQUERYREALFUNDJOURLISTREQUEST,
  '__module__' : 'trade.request.TradeQueryRealFundJourListRequest_pb2'
  # @@protoc_insertion_point(class_scope:TradeQueryRealFundJourListRequest)
  })
_sym_db.RegisterMessage(TradeQueryRealFundJourListRequest)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
