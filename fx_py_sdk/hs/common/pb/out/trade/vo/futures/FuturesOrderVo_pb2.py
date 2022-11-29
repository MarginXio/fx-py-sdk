# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trade/vo/futures/FuturesOrderVo.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='trade/vo/futures/FuturesOrderVo.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n5com.huasheng.quant.open.sdk.protobuf.trade.vo.futuresB\023FuturesOrderVoProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%trade/vo/futures/FuturesOrderVo.proto\"\xea\x03\n\x0e\x46uturesOrderVo\x12\x11\n\tstockCode\x18\x01 \x01(\t\x12\x11\n\tstockName\x18\x02 \x01(\t\x12\x15\n\rbusinessPrice\x18\x03 \x01(\t\x12\x11\n\tentrustBs\x18\x04 \x01(\t\x12\x14\n\x0c\x65ntrustPrice\x18\x05 \x01(\t\x12\x15\n\rentrustAmount\x18\x07 \x01(\t\x12\x16\n\x0e\x62usinessAmount\x18\x08 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\t \x01(\t\x12\x14\n\x0c\x62usinessTime\x18\n \x01(\t\x12\x13\n\x0b\x65ntrustTime\x18\x0b \x01(\t\x12\x15\n\rqueryParamStr\x18\x0c \x01(\t\x12\x12\n\nstatusDesc\x18\r \x01(\t\x12\x0e\n\x06status\x18\x0e \x01(\t\x12\x11\n\tentrustId\x18\x0f \x01(\t\x12\x15\n\rcanBeCanceled\x18\x11 \x01(\x05\x12\x13\n\x0b\x65ntrustType\x18\x12 \x01(\t\x12\x16\n\x0e\x65ntrustTypeNum\x18\x14 \x01(\t\x12\x0f\n\x07isValid\x18\x15 \x01(\x05\x12\x14\n\x0c\x63\x61nBeUpdated\x18\x18 \x01(\x05\x12\x11\n\tvalidType\x18\x16 \x01(\t\x12\x15\n\rvalidTypeDesc\x18\x17 \x01(\t\x12\x14\n\x0corderOptions\x18\x19 \x01(\x05\x12\x11\n\tvalidTime\x18\x1a \x01(\tBL\n5com.huasheng.quant.open.sdk.protobuf.trade.vo.futuresB\x13\x46uturesOrderVoProtob\x06proto3'
)




_FUTURESORDERVO = _descriptor.Descriptor(
  name='FuturesOrderVo',
  full_name='FuturesOrderVo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='stockCode', full_name='FuturesOrderVo.stockCode', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stockName', full_name='FuturesOrderVo.stockName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='businessPrice', full_name='FuturesOrderVo.businessPrice', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustBs', full_name='FuturesOrderVo.entrustBs', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustPrice', full_name='FuturesOrderVo.entrustPrice', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustAmount', full_name='FuturesOrderVo.entrustAmount', index=5,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='businessAmount', full_name='FuturesOrderVo.businessAmount', index=6,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date', full_name='FuturesOrderVo.date', index=7,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='businessTime', full_name='FuturesOrderVo.businessTime', index=8,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustTime', full_name='FuturesOrderVo.entrustTime', index=9,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queryParamStr', full_name='FuturesOrderVo.queryParamStr', index=10,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='statusDesc', full_name='FuturesOrderVo.statusDesc', index=11,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='FuturesOrderVo.status', index=12,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustId', full_name='FuturesOrderVo.entrustId', index=13,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='canBeCanceled', full_name='FuturesOrderVo.canBeCanceled', index=14,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustType', full_name='FuturesOrderVo.entrustType', index=15,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrustTypeNum', full_name='FuturesOrderVo.entrustTypeNum', index=16,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='isValid', full_name='FuturesOrderVo.isValid', index=17,
      number=21, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='canBeUpdated', full_name='FuturesOrderVo.canBeUpdated', index=18,
      number=24, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='validType', full_name='FuturesOrderVo.validType', index=19,
      number=22, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='validTypeDesc', full_name='FuturesOrderVo.validTypeDesc', index=20,
      number=23, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='orderOptions', full_name='FuturesOrderVo.orderOptions', index=21,
      number=25, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='validTime', full_name='FuturesOrderVo.validTime', index=22,
      number=26, type=9, cpp_type=9, label=1,
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
  serialized_start=42,
  serialized_end=532,
)

DESCRIPTOR.message_types_by_name['FuturesOrderVo'] = _FUTURESORDERVO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FuturesOrderVo = _reflection.GeneratedProtocolMessageType('FuturesOrderVo', (_message.Message,), {
  'DESCRIPTOR' : _FUTURESORDERVO,
  '__module__' : 'trade.vo.futures.FuturesOrderVo_pb2'
  # @@protoc_insertion_point(class_scope:FuturesOrderVo)
  })
_sym_db.RegisterMessage(FuturesOrderVo)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)