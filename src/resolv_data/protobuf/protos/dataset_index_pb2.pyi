from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DatasetIndex(_message.Message):
    __slots__ = ("id", "version", "entries")
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    id: str
    version: str
    entries: _containers.RepeatedCompositeFieldContainer[DatasetEntry]
    def __init__(self, id: _Optional[str] = ..., version: _Optional[str] = ..., entries: _Optional[_Iterable[_Union[DatasetEntry, _Mapping]]] = ...) -> None: ...

class DatasetEntry(_message.Message):
    __slots__ = ("id", "music_metadata", "files", "split")
    class FilesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: EntryFile
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[EntryFile, _Mapping]] = ...) -> None: ...
    class MusicTrackMetadata(_message.Message):
        __slots__ = ("composer", "title", "year", "duration", "release")
        COMPOSER_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        YEAR_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        RELEASE_FIELD_NUMBER: _ClassVar[int]
        composer: str
        title: str
        year: int
        duration: float
        release: str
        def __init__(self, composer: _Optional[str] = ..., title: _Optional[str] = ..., year: _Optional[int] = ..., duration: _Optional[float] = ..., release: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    MUSIC_METADATA_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    SPLIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    music_metadata: DatasetEntry.MusicTrackMetadata
    files: _containers.MessageMap[str, EntryFile]
    split: str
    def __init__(self, id: _Optional[str] = ..., music_metadata: _Optional[_Union[DatasetEntry.MusicTrackMetadata, _Mapping]] = ..., files: _Optional[_Mapping[str, EntryFile]] = ..., split: _Optional[str] = ...) -> None: ...

class EntryFile(_message.Message):
    __slots__ = ("path", "md5_checksum", "symbolic_music_attributes")
    class SymbolicMusicFileAttributes(_message.Message):
        __slots__ = ("match_score",)
        MATCH_SCORE_FIELD_NUMBER: _ClassVar[int]
        match_score: float
        def __init__(self, match_score: _Optional[float] = ...) -> None: ...
    PATH_FIELD_NUMBER: _ClassVar[int]
    MD5_CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    SYMBOLIC_MUSIC_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    path: str
    md5_checksum: str
    symbolic_music_attributes: EntryFile.SymbolicMusicFileAttributes
    def __init__(self, path: _Optional[str] = ..., md5_checksum: _Optional[str] = ..., symbolic_music_attributes: _Optional[_Union[EntryFile.SymbolicMusicFileAttributes, _Mapping]] = ...) -> None: ...
