# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common/msg/Response.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from common.constant import ResponseMsgType_pb2 as common_dot_constant_dot_ResponseMsgType__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='common/msg/Response.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n/com.huasheng.quant.open.sdk.protobuf.common.msgB\rResponseProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x19\x63ommon/msg/Response.proto\x1a\x19google/protobuf/any.proto\x1a%common/constant/ResponseMsgType.proto\"\xb2\x01\n\nPBResponse\x12)\n\x0fresponseMsgType\x18\x01 \x01(\x0e\x32\x10.ResponseMsgType\x12\x11\n\trequestId\x18\x02 \x01(\t\x12\x14\n\x0cresponseTime\x18\x03 \x01(\x03\x12\x14\n\x0cresponseCode\x18\x04 \x01(\t\x12\x13\n\x0bresponseMsg\x18\x05 \x01(\t\x12%\n\x07payload\x18\x06 \x01(\x0b\x32\x14.google.protobuf.AnyB@\n/com.huasheng.quant.open.sdk.protobuf.common.msgB\rResponseProtob\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,common_dot_constant_dot_ResponseMsgType__pb2.DESCRIPTOR,])




_PBRESPONSE = _descriptor.Descriptor(
  name='PBResponse',
  full_name='PBResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='responseMsgType', full_name='PBResponse.responseMsgType', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='requestId', full_name='PBResponse.requestId', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='responseTime', full_name='PBResponse.responseTime', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='responseCode', full_name='PBResponse.responseCode', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='responseMsg', full_name='PBResponse.responseMsg', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload', full_name='PBResponse.payload', index=5,
      number=6, type=11, cpp_type=10, label=1,
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
  serialized_start=96,
  serialized_end=274,
)

_PBRESPONSE.fields_by_name['responseMsgType'].enum_type = common_dot_constant_dot_ResponseMsgType__pb2._RESPONSEMSGTYPE
_PBRESPONSE.fields_by_name['payload'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['PBResponse'] = _PBRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PBResponse = _reflection.GeneratedProtocolMessageType('PBResponse', (_message.Message,), {
  'DESCRIPTOR' : _PBRESPONSE,
  '__module__' : 'common.msg.Response_pb2'
  # @@protoc_insertion_point(class_scope:PBResponse)
  })
_sym_db.RegisterMessage(PBResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
