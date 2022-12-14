# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trade/response/TradeQueryMarginFundInfoResponse.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='trade/response/TradeQueryMarginFundInfoResponse.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n3com.huasheng.quant.open.sdk.protobuf.trade.responseB%TradeQueryMarginFundInfoResponseProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n5trade/response/TradeQueryMarginFundInfoResponse.proto\"\x8f\x02\n TradeQueryMarginFundInfoResponse\x12\x14\n\x0choldsBalance\x18\x01 \x01(\t\x12\x14\n\x0c\x61ssetBalance\x18\x02 \x01(\t\x12\x15\n\renableBalance\x18\x03 \x01(\t\x12\x13\n\x0bmarketValue\x18\x04 \x01(\t\x12\x12\n\ncashOnHold\x18\x05 \x01(\t\x12\x13\n\x0b\x63reditValue\x18\x06 \x01(\t\x12\x12\n\ncreditLine\x18\x07 \x01(\t\x12\x14\n\x0c\x66\x65tchBalance\x18\x08 \x01(\t\x12\x15\n\rfrozenBalance\x18\t \x01(\t\x12\x15\n\raccountStatus\x18\n \x01(\t\x12\x12\n\nspentRatio\x18\x0b \x01(\tB\\\n3com.huasheng.quant.open.sdk.protobuf.trade.responseB%TradeQueryMarginFundInfoResponseProtob\x06proto3'
)




_TRADEQUERYMARGINFUNDINFORESPONSE = _descriptor.Descriptor(
  name='TradeQueryMarginFundInfoResponse',
  full_name='TradeQueryMarginFundInfoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='holdsBalance', full_name='TradeQueryMarginFundInfoResponse.holdsBalance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='assetBalance', full_name='TradeQueryMarginFundInfoResponse.assetBalance', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enableBalance', full_name='TradeQueryMarginFundInfoResponse.enableBalance', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='marketValue', full_name='TradeQueryMarginFundInfoResponse.marketValue', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cashOnHold', full_name='TradeQueryMarginFundInfoResponse.cashOnHold', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='creditValue', full_name='TradeQueryMarginFundInfoResponse.creditValue', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='creditLine', full_name='TradeQueryMarginFundInfoResponse.creditLine', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fetchBalance', full_name='TradeQueryMarginFundInfoResponse.fetchBalance', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frozenBalance', full_name='TradeQueryMarginFundInfoResponse.frozenBalance', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='accountStatus', full_name='TradeQueryMarginFundInfoResponse.accountStatus', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='spentRatio', full_name='TradeQueryMarginFundInfoResponse.spentRatio', index=10,
      number=11, type=9, cpp_type=9, label=1,
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
  serialized_start=58,
  serialized_end=329,
)

DESCRIPTOR.message_types_by_name['TradeQueryMarginFundInfoResponse'] = _TRADEQUERYMARGINFUNDINFORESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TradeQueryMarginFundInfoResponse = _reflection.GeneratedProtocolMessageType('TradeQueryMarginFundInfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _TRADEQUERYMARGINFUNDINFORESPONSE,
  '__module__' : 'trade.response.TradeQueryMarginFundInfoResponse_pb2'
  # @@protoc_insertion_point(class_scope:TradeQueryMarginFundInfoResponse)
  })
_sym_db.RegisterMessage(TradeQueryMarginFundInfoResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
