# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hq/response/OrderBookResponse.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hq.dto import Security_pb2 as hq_dot_dto_dot_Security__pb2
from hq.dto import OrderBook_pb2 as hq_dot_dto_dot_OrderBook__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hq/response/OrderBookResponse.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n0com.huasheng.quant.open.sdk.protobuf.hq.responseB\026OrderBookResponseProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n#hq/response/OrderBookResponse.proto\x1a\x15hq/dto/Security.proto\x1a\x16hq/dto/OrderBook.proto\"\x91\x01\n\x11OrderBookResponse\x12\x1b\n\x08security\x18\x01 \x01(\x0b\x32\t.Security\x12$\n\x10orderBookAskList\x18\x02 \x03(\x0b\x32\n.OrderBook\x12$\n\x10orderBookBidList\x18\x03 \x03(\x0b\x32\n.OrderBook\x12\x13\n\x0bspreadLevel\x18\x04 \x01(\x01\x42J\n0com.huasheng.quant.open.sdk.protobuf.hq.responseB\x16OrderBookResponseProtob\x06proto3'
  ,
  dependencies=[hq_dot_dto_dot_Security__pb2.DESCRIPTOR,hq_dot_dto_dot_OrderBook__pb2.DESCRIPTOR,])




_ORDERBOOKRESPONSE = _descriptor.Descriptor(
  name='OrderBookResponse',
  full_name='OrderBookResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='security', full_name='OrderBookResponse.security', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='orderBookAskList', full_name='OrderBookResponse.orderBookAskList', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='orderBookBidList', full_name='OrderBookResponse.orderBookBidList', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='spreadLevel', full_name='OrderBookResponse.spreadLevel', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=87,
  serialized_end=232,
)

_ORDERBOOKRESPONSE.fields_by_name['security'].message_type = hq_dot_dto_dot_Security__pb2._SECURITY
_ORDERBOOKRESPONSE.fields_by_name['orderBookAskList'].message_type = hq_dot_dto_dot_OrderBook__pb2._ORDERBOOK
_ORDERBOOKRESPONSE.fields_by_name['orderBookBidList'].message_type = hq_dot_dto_dot_OrderBook__pb2._ORDERBOOK
DESCRIPTOR.message_types_by_name['OrderBookResponse'] = _ORDERBOOKRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OrderBookResponse = _reflection.GeneratedProtocolMessageType('OrderBookResponse', (_message.Message,), {
  'DESCRIPTOR' : _ORDERBOOKRESPONSE,
  '__module__' : 'hq.response.OrderBookResponse_pb2'
  # @@protoc_insertion_point(class_scope:OrderBookResponse)
  })
_sym_db.RegisterMessage(OrderBookResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
