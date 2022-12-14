# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hq/notify/TickerNotify.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hq.dto import Security_pb2 as hq_dot_dto_dot_Security__pb2
from hq.dto import Ticker_pb2 as hq_dot_dto_dot_Ticker__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hq/notify/TickerNotify.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n.com.huasheng.quant.open.sdk.protobuf.hq.notifyB\021TickerNotifyProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1chq/notify/TickerNotify.proto\x1a\x15hq/dto/Security.proto\x1a\x13hq/dto/Ticker.proto\"D\n\x0cTickerNotify\x12\x1b\n\x08security\x18\x01 \x01(\x0b\x32\t.Security\x12\x17\n\x06ticker\x18\x02 \x01(\x0b\x32\x07.TickerBC\n.com.huasheng.quant.open.sdk.protobuf.hq.notifyB\x11TickerNotifyProtob\x06proto3'
  ,
  dependencies=[hq_dot_dto_dot_Security__pb2.DESCRIPTOR,hq_dot_dto_dot_Ticker__pb2.DESCRIPTOR,])




_TICKERNOTIFY = _descriptor.Descriptor(
  name='TickerNotify',
  full_name='TickerNotify',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='security', full_name='TickerNotify.security', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ticker', full_name='TickerNotify.ticker', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=76,
  serialized_end=144,
)

_TICKERNOTIFY.fields_by_name['security'].message_type = hq_dot_dto_dot_Security__pb2._SECURITY
_TICKERNOTIFY.fields_by_name['ticker'].message_type = hq_dot_dto_dot_Ticker__pb2._TICKER
DESCRIPTOR.message_types_by_name['TickerNotify'] = _TICKERNOTIFY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TickerNotify = _reflection.GeneratedProtocolMessageType('TickerNotify', (_message.Message,), {
  'DESCRIPTOR' : _TICKERNOTIFY,
  '__module__' : 'hq.notify.TickerNotify_pb2'
  # @@protoc_insertion_point(class_scope:TickerNotify)
  })
_sym_db.RegisterMessage(TickerNotify)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
