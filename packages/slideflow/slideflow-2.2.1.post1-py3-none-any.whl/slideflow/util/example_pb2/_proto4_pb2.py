# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rexample.proto\x12\x08tfrecord\"\x1a\n\tBytesList\x12\r\n\x05value\x18\x01 \x03(\x0c\"\x1e\n\tFloatList\x12\x11\n\x05value\x18\x01 \x03(\x02\x42\x02\x10\x01\"\x1e\n\tInt64List\x12\x11\n\x05value\x18\x01 \x03(\x03\x42\x02\x10\x01\"\x92\x01\n\x07\x46\x65\x61ture\x12)\n\nbytes_list\x18\x01 \x01(\x0b\x32\x13.tfrecord.BytesListH\x00\x12)\n\nfloat_list\x18\x02 \x01(\x0b\x32\x13.tfrecord.FloatListH\x00\x12)\n\nint64_list\x18\x03 \x01(\x0b\x32\x13.tfrecord.Int64ListH\x00\x42\x06\n\x04kind\"\x7f\n\x08\x46\x65\x61tures\x12\x30\n\x07\x66\x65\x61ture\x18\x01 \x03(\x0b\x32\x1f.tfrecord.Features.FeatureEntry\x1a\x41\n\x0c\x46\x65\x61tureEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12 \n\x05value\x18\x02 \x01(\x0b\x32\x11.tfrecord.Feature:\x02\x38\x01\"1\n\x0b\x46\x65\x61tureList\x12\"\n\x07\x66\x65\x61ture\x18\x01 \x03(\x0b\x32\x11.tfrecord.Feature\"\x98\x01\n\x0c\x46\x65\x61tureLists\x12=\n\x0c\x66\x65\x61ture_list\x18\x01 \x03(\x0b\x32\'.tfrecord.FeatureLists.FeatureListEntry\x1aI\n\x10\x46\x65\x61tureListEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12$\n\x05value\x18\x02 \x01(\x0b\x32\x15.tfrecord.FeatureList:\x02\x38\x01\"/\n\x07\x45xample\x12$\n\x08\x66\x65\x61tures\x18\x01 \x01(\x0b\x32\x12.tfrecord.Features\"e\n\x0fSequenceExample\x12#\n\x07\x63ontext\x18\x01 \x01(\x0b\x32\x12.tfrecord.Features\x12-\n\rfeature_lists\x18\x02 \x01(\x0b\x32\x16.tfrecord.FeatureListsB\x03\xf8\x01\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    raise ValueError('Invalid protobuf module descriptor for example_pb2')
# @@protoc_insertion_point(module_scope)
