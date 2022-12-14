# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hq/response/BrokerResponse.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hq.dto import Security_pb2 as hq_dot_dto_dot_Security__pb2
from hq.dto import Broker_pb2 as hq_dot_dto_dot_Broker__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hq/response/BrokerResponse.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n0com.huasheng.quant.open.sdk.protobuf.hq.responseB\023BrokerResponseProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n hq/response/BrokerResponse.proto\x1a\x15hq/dto/Security.proto\x1a\x13hq/dto/Broker.proto\"m\n\x0e\x42rokerResponse\x12\x1b\n\x08security\x18\x01 \x01(\x0b\x32\t.Security\x12\x1e\n\rbrokerAskList\x18\x02 \x03(\x0b\x32\x07.Broker\x12\x1e\n\rbrokerBidList\x18\x03 \x03(\x0b\x32\x07.BrokerBG\n0com.huasheng.quant.open.sdk.protobuf.hq.responseB\x13\x42rokerResponseProtob\x06proto3'
  ,
  dependencies=[hq_dot_dto_dot_Security__pb2.DESCRIPTOR,hq_dot_dto_dot_Broker__pb2.DESCRIPTOR,])




_BROKERRESPONSE = _descriptor.Descriptor(
  name='BrokerResponse',
  full_name='BrokerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='security', full_name='BrokerResponse.security', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='brokerAskList', full_name='BrokerResponse.brokerAskList', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='brokerBidList', full_name='BrokerResponse.brokerBidList', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=80,
  serialized_end=189,
)

_BROKERRESPONSE.fields_by_name['security'].message_type = hq_dot_dto_dot_Security__pb2._SECURITY
_BROKERRESPONSE.fields_by_name['brokerAskList'].message_type = hq_dot_dto_dot_Broker__pb2._BROKER
_BROKERRESPONSE.fields_by_name['brokerBidList'].message_type = hq_dot_dto_dot_Broker__pb2._BROKER
DESCRIPTOR.message_types_by_name['BrokerResponse'] = _BROKERRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BrokerResponse = _reflection.GeneratedProtocolMessageType('BrokerResponse', (_message.Message,), {
  'DESCRIPTOR' : _BROKERRESPONSE,
  '__module__' : 'hq.response.BrokerResponse_pb2'
  # @@protoc_insertion_point(class_scope:BrokerResponse)
  })
_sym_db.RegisterMessage(BrokerResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
