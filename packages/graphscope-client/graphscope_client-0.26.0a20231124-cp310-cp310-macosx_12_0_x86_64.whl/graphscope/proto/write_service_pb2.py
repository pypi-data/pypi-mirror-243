# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: write_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13write_service.proto\x12\x0cgs.rpc.groot\"\x14\n\x12GetClientIdRequest\"(\n\x13GetClientIdResponse\x12\x11\n\tclient_id\x18\x01 \x01(\t\"\\\n\x11\x42\x61tchWriteRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x34\n\x0ewrite_requests\x18\x02 \x03(\x0b\x32\x1c.gs.rpc.groot.WriteRequestPb\")\n\x12\x42\x61tchWriteResponse\x12\x13\n\x0bsnapshot_id\x18\x01 \x01(\x03\"?\n\x12RemoteFlushRequest\x12\x13\n\x0bsnapshot_id\x18\x01 \x01(\x03\x12\x14\n\x0cwait_time_ms\x18\x02 \x01(\x03\"&\n\x13RemoteFlushResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"p\n\x0eWriteRequestPb\x12-\n\nwrite_type\x18\x01 \x01(\x0e\x32\x19.gs.rpc.groot.WriteTypePb\x12/\n\x0b\x64\x61ta_record\x18\x02 \x01(\x0b\x32\x1a.gs.rpc.groot.DataRecordPb\"\x87\x02\n\x0c\x44\x61taRecordPb\x12<\n\x11vertex_record_key\x18\x01 \x01(\x0b\x32\x1f.gs.rpc.groot.VertexRecordKeyPbH\x00\x12\x38\n\x0f\x65\x64ge_record_key\x18\x02 \x01(\x0b\x32\x1d.gs.rpc.groot.EdgeRecordKeyPbH\x00\x12>\n\nproperties\x18\x03 \x03(\x0b\x32*.gs.rpc.groot.DataRecordPb.PropertiesEntry\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x0c\n\nrecord_key\"\xa1\x01\n\x11VertexRecordKeyPb\x12\r\n\x05label\x18\x01 \x01(\t\x12H\n\rpk_properties\x18\x02 \x03(\x0b\x32\x31.gs.rpc.groot.VertexRecordKeyPb.PkPropertiesEntry\x1a\x33\n\x11PkPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xa4\x01\n\x0f\x45\x64geRecordKeyPb\x12\r\n\x05label\x18\x01 \x01(\t\x12\x37\n\x0esrc_vertex_key\x18\x02 \x01(\x0b\x32\x1f.gs.rpc.groot.VertexRecordKeyPb\x12\x37\n\x0e\x64st_vertex_key\x18\x03 \x01(\x0b\x32\x1f.gs.rpc.groot.VertexRecordKeyPb\x12\x10\n\x08inner_id\x18\x04 \x01(\x03*R\n\x0bWriteTypePb\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06INSERT\x10\x01\x12\n\n\x06UPDATE\x10\x02\x12\n\n\x06\x44\x45LETE\x10\x03\x12\x12\n\x0e\x43LEAR_PROPERTY\x10\x04\x32\x86\x02\n\x0b\x43lientWrite\x12R\n\x0bgetClientId\x12 .gs.rpc.groot.GetClientIdRequest\x1a!.gs.rpc.groot.GetClientIdResponse\x12O\n\nbatchWrite\x12\x1f.gs.rpc.groot.BatchWriteRequest\x1a .gs.rpc.groot.BatchWriteResponse\x12R\n\x0bremoteFlush\x12 .gs.rpc.groot.RemoteFlushRequest\x1a!.gs.rpc.groot.RemoteFlushResponseB&\n\"com.alibaba.graphscope.proto.grootP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'write_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\"com.alibaba.graphscope.proto.grootP\001'
  _DATARECORDPB_PROPERTIESENTRY._options = None
  _DATARECORDPB_PROPERTIESENTRY._serialized_options = b'8\001'
  _VERTEXRECORDKEYPB_PKPROPERTIESENTRY._options = None
  _VERTEXRECORDKEYPB_PKPROPERTIESENTRY._serialized_options = b'8\001'
  _globals['_WRITETYPEPB']._serialized_start=1054
  _globals['_WRITETYPEPB']._serialized_end=1136
  _globals['_GETCLIENTIDREQUEST']._serialized_start=37
  _globals['_GETCLIENTIDREQUEST']._serialized_end=57
  _globals['_GETCLIENTIDRESPONSE']._serialized_start=59
  _globals['_GETCLIENTIDRESPONSE']._serialized_end=99
  _globals['_BATCHWRITEREQUEST']._serialized_start=101
  _globals['_BATCHWRITEREQUEST']._serialized_end=193
  _globals['_BATCHWRITERESPONSE']._serialized_start=195
  _globals['_BATCHWRITERESPONSE']._serialized_end=236
  _globals['_REMOTEFLUSHREQUEST']._serialized_start=238
  _globals['_REMOTEFLUSHREQUEST']._serialized_end=301
  _globals['_REMOTEFLUSHRESPONSE']._serialized_start=303
  _globals['_REMOTEFLUSHRESPONSE']._serialized_end=341
  _globals['_WRITEREQUESTPB']._serialized_start=343
  _globals['_WRITEREQUESTPB']._serialized_end=455
  _globals['_DATARECORDPB']._serialized_start=458
  _globals['_DATARECORDPB']._serialized_end=721
  _globals['_DATARECORDPB_PROPERTIESENTRY']._serialized_start=658
  _globals['_DATARECORDPB_PROPERTIESENTRY']._serialized_end=707
  _globals['_VERTEXRECORDKEYPB']._serialized_start=724
  _globals['_VERTEXRECORDKEYPB']._serialized_end=885
  _globals['_VERTEXRECORDKEYPB_PKPROPERTIESENTRY']._serialized_start=834
  _globals['_VERTEXRECORDKEYPB_PKPROPERTIESENTRY']._serialized_end=885
  _globals['_EDGERECORDKEYPB']._serialized_start=888
  _globals['_EDGERECORDKEYPB']._serialized_end=1052
  _globals['_CLIENTWRITE']._serialized_start=1139
  _globals['_CLIENTWRITE']._serialized_end=1401
# @@protoc_insertion_point(module_scope)
