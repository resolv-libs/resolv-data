# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: resolv_data/protobuf/protos/dataset_index.proto
# Protobuf Python Version: 4.25.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/resolv_data/protobuf/protos/dataset_index.proto\"?\n\x0c\x44\x61tasetIndex\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x1e\n\x07\x65ntries\x18\x02 \x03(\x0b\x32\r.DatasetEntry\"\xbc\x02\n\x0c\x44\x61tasetEntry\x12\n\n\x02id\x18\x01 \x01(\t\x12:\n\x0emusic_metadata\x18\x02 \x01(\x0b\x32 .DatasetEntry.MusicTrackMetadataH\x00\x12\'\n\x05\x66iles\x18\x03 \x03(\x0b\x32\x18.DatasetEntry.FilesEntry\x12\r\n\x05split\x18\x04 \x01(\t\x1a\x38\n\nFilesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x19\n\x05value\x18\x02 \x01(\x0b\x32\n.EntryFile:\x02\x38\x01\x1a\x66\n\x12MusicTrackMetadata\x12\x10\n\x08\x63omposer\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0c\n\x04year\x18\x04 \x01(\x05\x12\x10\n\x08\x64uration\x18\x05 \x01(\x01\x12\x0f\n\x07release\x18\x06 \x01(\tB\n\n\x08metadata\"\xbe\x01\n\tEntryFile\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x14\n\x0cmd5_checksum\x18\x02 \x01(\t\x12K\n\x19symbolic_music_attributes\x18\x03 \x01(\x0b\x32&.EntryFile.SymbolicMusicFileAttributesH\x00\x1a\x32\n\x1bSymbolicMusicFileAttributes\x12\x13\n\x0bmatch_score\x18\x01 \x01(\x01\x42\x0c\n\nattributesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'resolv_data.protobuf.protos.dataset_index_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DATASETENTRY_FILESENTRY']._options = None
  _globals['_DATASETENTRY_FILESENTRY']._serialized_options = b'8\001'
  _globals['_DATASETINDEX']._serialized_start=51
  _globals['_DATASETINDEX']._serialized_end=114
  _globals['_DATASETENTRY']._serialized_start=117
  _globals['_DATASETENTRY']._serialized_end=433
  _globals['_DATASETENTRY_FILESENTRY']._serialized_start=261
  _globals['_DATASETENTRY_FILESENTRY']._serialized_end=317
  _globals['_DATASETENTRY_MUSICTRACKMETADATA']._serialized_start=319
  _globals['_DATASETENTRY_MUSICTRACKMETADATA']._serialized_end=421
  _globals['_ENTRYFILE']._serialized_start=436
  _globals['_ENTRYFILE']._serialized_end=626
  _globals['_ENTRYFILE_SYMBOLICMUSICFILEATTRIBUTES']._serialized_start=562
  _globals['_ENTRYFILE_SYMBOLICMUSICFILEATTRIBUTES']._serialized_end=612
# @@protoc_insertion_point(module_scope)