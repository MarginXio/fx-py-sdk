# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trade/response/TradeQueryRealDeliverListResponse.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hs.common.pb.trade.vo import OrderVo_pb2 as trade_dot_vo_dot_OrderVo__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='trade/response/TradeQueryRealDeliverListResponse.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n3com.huasheng.quant.open.sdk.protobuf.trade.responseB&TradeQueryRealDeliverListResponseProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n6trade/response/TradeQueryRealDeliverListResponse.proto\x1a\x16trade/vo/OrderVo.proto\";\n!TradeQueryRealDeliverListResponse\x12\x16\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x08.OrderVoB]\n3com.huasheng.quant.open.sdk.protobuf.trade.responseB&TradeQueryRealDeliverListResponseProtob\x06proto3'
  ,
  dependencies=[trade_dot_vo_dot_OrderVo__pb2.DESCRIPTOR,])




_TRADEQUERYREALDELIVERLISTRESPONSE = _descriptor.Descriptor(
  name='TradeQueryRealDeliverListResponse',
  full_name='TradeQueryRealDeliverListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='TradeQueryRealDeliverListResponse.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=82,
  serialized_end=141,
)

_TRADEQUERYREALDELIVERLISTRESPONSE.fields_by_name['data'].message_type = trade_dot_vo_dot_OrderVo__pb2._ORDERVO
DESCRIPTOR.message_types_by_name['TradeQueryRealDeliverListResponse'] = _TRADEQUERYREALDELIVERLISTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TradeQueryRealDeliverListResponse = _reflection.GeneratedProtocolMessageType('TradeQueryRealDeliverListResponse', (_message.Message,), {
  'DESCRIPTOR' : _TRADEQUERYREALDELIVERLISTRESPONSE,
  '__module__' : 'trade.response.TradeQueryRealDeliverListResponse_pb2'
  # @@protoc_insertion_point(class_scope:TradeQueryRealDeliverListResponse)
  })
_sym_db.RegisterMessage(TradeQueryRealDeliverListResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
