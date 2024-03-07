"""
Module Name: midi.py.
Description: Data Adapter for MusicXML files.
Author: Matteo Pettenò.
Copyright (c) 2024, Matteo Pettenò
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""
from typing import Any

from resolv_data.canonical.base import DataAdapter
from resolv_mir import NoteSequence
from resolv_mir.note_sequence.io import musicxml_io


class MusicXMLDocumentAdapter(DataAdapter[NoteSequence]):

    def to_canonical_message(self, source_type: str, content: Any, metadata: Any) -> NoteSequence:
        return musicxml_io.musicxml_to_note_sequence(content, source_type)

    def to_source_format(self, canonical_message: NoteSequence, **kwargs) -> Any:
        # TODO - Data adapter: MusicXML to NoteSequence implementation
        return None