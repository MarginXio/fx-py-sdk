# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trade/request/TradeQueryHistoryDeliverListRequest.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='trade/request/TradeQueryHistoryDeliverListRequest.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n2com.huasheng.quant.open.sdk.protobuf.trade.requestB(TradeQueryHistoryDeliverListRequestProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n7trade/request/TradeQueryHistoryDeliverListRequest.proto\"\x8a\x01\n#TradeQueryHistoryDeliverListRequest\x12\x14\n\x0c\x65xchangeType\x18\x01 \x01(\t\x12\x15\n\rqueryParamStr\x18\x02 \x01(\t\x12\x12\n\nqueryCount\x18\x03 \x01(\x05\x12\x11\n\tstartDate\x18\x04 \x01(\t\x12\x0f\n\x07\x65ndDate\x18\x05 \x01(\tB^\n2com.huasheng.quant.open.sdk.protobuf.trade.requestB(TradeQueryHistoryDeliverListRequestProtob\x06proto3'
)




_TRADEQUERYHISTORYDELIVERLISTREQUEST = _descriptor.Descriptor(
  name='TradeQueryHistoryDeliverListRequest',
  full_name='TradeQueryHistoryDeliverListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='exchangeType', full_name='TradeQueryHistoryDeliverListRequest.exchangeType', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queryParamStr', full_name='TradeQueryHistoryDeliverListRequest.queryParamStr', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queryCount', full_name='TradeQueryHistoryDeliverListRequest.queryCount', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='startDate', full_name='TradeQueryHistoryDeliverListRequest.startDate', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='endDate', full_name='TradeQueryHistoryDeliverListRequest.endDate', index=4,
      number=5, type=9, cpp_type=9, label=1,
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
  serialized_start=60,
  serialized_end=198,
)

DESCRIPTOR.message_types_by_name['TradeQueryHistoryDeliverListRequest'] = _TRADEQUERYHISTORYDELIVERLISTREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TradeQueryHistoryDeliverListRequest = _reflection.GeneratedProtocolMessageType('TradeQueryHistoryDeliverListRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRADEQUERYHISTORYDELIVERLISTREQUEST,
  '__module__' : 'trade.request.TradeQueryHistoryDeliverListRequest_pb2'
  # @@protoc_insertion_point(class_scope:TradeQueryHistoryDeliverListRequest)
  })
_sym_db.RegisterMessage(TradeQueryHistoryDeliverListRequest)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)