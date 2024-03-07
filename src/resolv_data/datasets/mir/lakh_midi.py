"""
Module Name: lakh_midi.py.
Description: Lakh MIDI Dataset.
Author: Matteo Pettenò.
Copyright (c) 2024, Matteo Pettenò
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""
import json
import os
import tables
from pathlib import Path
from typing import Dict, List, Union

from resolv_data import utilities
from resolv_data.base import DatasetInfo, DirectoryDataset, RemoteSource
from resolv_data.protobuf import DatasetIndex, DatasetEntry, EntryFile

_NAME = "Lakh MIDI"

_DESCRIPTION = """\
The Lakh MIDI dataset is a collection of 176,581 unique MIDI files, 45,129 of \
which have been matched and aligned to entries in the Million Song Dataset. \
Its goal is to facilitate large-scale music information retrieval, both \
symbolic (using the MIDI files alone) and audio content-based (using \
information extracted from the MIDI files as annotations for the matched \
audio files)."""

_HOMEPAGE = "https://colinraffel.com/projects/lmd/"

_LICENSE_INFO = "Creative Commons Attribution 4.0 International License (CC-By 4.0)"

_CITATION = """\
@phdthesis{raffel2016learning,
  author={Colin Raffel},
  title={Learning-Based Methods for Comparing Sequences, with Applications to Audio-to-{MIDI} Alignment and Matching},
  year=2016
}"""


class LakhMIDIDatasetV1(DirectoryDataset):

    @staticmethod
    def remote_sources() -> Dict[str, List[RemoteSource]]:
        lmd_matched_resource = RemoteSource(
            filename="lmd_matched.tar.gz",
            url="http://hog.ee.columbia.edu/craffel/lmd/lmd_matched.tar.gz",
            checksum="621ff830aed771f469e5bfa13dc12a33c6ed69090adeda63d0b5c47783af0191",
            checksum_type="sha256",
            main_source=True,
            archive=True,
            has_archived_root=True
        )
        match_scores_resource = RemoteSource(
            filename="match_scores.json",
            url="http://hog.ee.columbia.edu/craffel/lmd/match_scores.json",
            checksum="267bc606dfa21f0ad0601a4a080972cd4ae8088fe4003b9bb2811b5be060a102",
            checksum_type="sha256"
        )
        return {
            "full": [
                RemoteSource(
                    filename="lmd_full.tar.gz",
                    url="http://hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz",
                    checksum="6fcfe2ac49ca08f3f214cec86ab138d4fc4dabcd7f27f491a838dae6db45a12b",
                    checksum_type="sha256",
                    main_source=True,
                    archive=True,
                    has_archived_root=True
                ),
                RemoteSource(
                    filename="md5_to_paths.json",
                    url="http://hog.ee.columbia.edu/craffel/lmd/md5_to_paths.json",
                    checksum="9002b7723f3edeca779e91688802fdd283b8df0c278162a4040f95bde5895805",
                    checksum_type="sha256"
                )
            ],
            "matched": [
                lmd_matched_resource,
                match_scores_resource
            ],
            "matched_with_msd_metadata": [
                lmd_matched_resource,
                match_scores_resource,
                RemoteSource(
                    filename="msd_h5_metadata.tar.gz",
                    url="http://hog.ee.columbia.edu/craffel/lmd/lmd_matched_h5.tar.gz",
                    checksum="049c62c0d90c7fd2a29352a1c745d12fb53019dcf2e74a3b29953f046aef3d1b",
                    checksum_type="sha256",
                    archive=True,
                    has_archived_root=True
                )
            ],
            "aligned": [
                RemoteSource(
                    filename="lmd_aligned.tar.gz",
                    url="http://hog.ee.columbia.edu/craffel/lmd/lmd_aligned.tar.gz",
                    checksum="2bf5400e82eba73204644946515489b68811e1e656b0cfd854efc14377f6e53b",
                    checksum_type="sha256",
                    main_source=True,
                    archive=True,
                    has_archived_root=True
                ),
                match_scores_resource
            ],
            "clean": [
                RemoteSource(
                    filename="lmd_clean_midi.tar.gz",
                    url="http://hog.ee.columbia.edu/craffel/lmd/clean_midi.tar.gz",
                    checksum="de1bb64cbc0cf35545a05b5c3e786aa6890cfa144edffc4b827ff41bf8c33dc5",
                    checksum_type="sha256",
                    main_source=True,
                    archive=True,
                    has_archived_root=True
                )
            ]
        }

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def info(self) -> DatasetInfo:
        return DatasetInfo(
            name=_NAME,
            version=self.version,
            description=_DESCRIPTION,
            homepage=_HOMEPAGE,
            license_info=_LICENSE_INFO,
            citation=_CITATION
        )

    @property
    def midi_filenames_path(self) -> Path:
        return self._root_dir / 'md5_to_paths.json'

    @property
    def match_scores_path(self) -> Path:
        return self._root_dir / 'match_scores.json'

    def _compute_index_internal(self, path_prefix: Union[str, Path]) -> DatasetIndex:
        path_prefix = path_prefix if path_prefix is not None else self._root_dir
        if self._mode == 'full':
            return self._compute_full_mode_index(path_prefix)
        elif self._mode == 'clean':
            return self._compute_clean_mode_index(path_prefix)
        else:
            return self._compute_matched_mode_index(path_prefix)

    def _compute_full_mode_index(self, path_prefix: Union[str, Path]) -> DatasetIndex:
        def build_track_proto(midi_file):
            track_id = midi_filenames[midi_file.stem][0]
            track_files = {
                'midi': EntryFile(path=f'{str(path_prefix)}/{str(midi_file.relative_to(self._root_dir))}',
                                  md5_checksum=utilities.compute_checksum(midi_file, checksum_type='md5'))
            }
            return DatasetEntry(id=track_id, files=track_files)

        with open(self.midi_filenames_path, 'r') as f:
            midi_filenames = json.load(f)

        return DatasetIndex(
            version=self.version,
            entries=[build_track_proto(midi_file) for midi_file in self._root_dir.glob('**/*.mid')]
        )

    def _compute_clean_mode_index(self, path_prefix: Union[str, Path]) -> DatasetIndex:
        def build_track_proto(midi_file):
            track_id = f'{midi_file.parent.name.replace(" ", "_").lower()}/{midi_file.name.replace(" ", "_").lower()}'
            track_metadata = DatasetEntry.MusicTrackMetadata(
                composer=midi_file.parent.name,
                title=midi_file.name
            )
            track_files = {
                'midi': EntryFile(path=f'{str(path_prefix)}/{str(midi_file.relative_to(self._root_dir))}',
                                  md5_checksum=utilities.compute_checksum(midi_file, checksum_type='md5'))
            }
            return DatasetEntry(id=track_id, music_metadata=track_metadata, files=track_files)

        return DatasetIndex(
            version=self.version,
            entries=[build_track_proto(midi_file) for midi_file in self._root_dir.glob('**/*.mid')]
        )

    def _compute_matched_mode_index(self, path_prefix: Union[str, Path]) -> DatasetIndex:
        def msd_id_to_dirs(msd_id):
            """Given an MSD ID, generate the path prefix.
            E.g. TRABCD12345678 -> A/B/C/TRABCD12345678"""
            return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)

        def build_track_proto(midi_file):
            track_id = midi_file.parent.name
            match_score = match_scores[track_id][midi_file.stem]
            track_metadata = None
            track_files = {
                'midi': EntryFile(path=f'{str(path_prefix)}/{str(midi_file.relative_to(self._root_dir))}',
                                  md5_checksum=utilities.compute_checksum(midi_file, checksum_type='md5'),
                                  symbolic_music_attributes=EntryFile.SymbolicMusicFileAttributes(
                                      match_score=match_score
                                  ))
            }

            if self._mode == 'matched_with_msd_metadata':
                msd_h5_metadata_dir = self.remote_sources['matched_with_msd_metadata'][2].filename.split('.')[0]
                msd_h5_metadata_path = self._root_dir / msd_h5_metadata_dir
                track_dirs = msd_id_to_dirs(track_id)
                h5_file_abs_path = f'{msd_h5_metadata_path}/{track_dirs}.h5'
                with tables.open_file(h5_file_abs_path) as h5:
                    track_metadata = DatasetEntry.MusicTrackMetadata(
                        composer=h5.root.metadata.songs.cols.artist_name[0],
                        title=h5.root.metadata.songs.cols.title[0],
                        year=h5.root.musicbrainz.songs.cols.year[0],
                        duration=h5.root.analysis.songs.cols.duration[0],
                        release=h5.root.metadata.songs.cols.release[0]
                    )
                track_files['features'] = EntryFile(
                    path=f'{str(path_prefix)}/{str(Path(h5_file_abs_path).relative_to(self._root_dir))}',
                    md5_checksum=utilities.compute_checksum(h5_file_abs_path, checksum_type='md5')
                )

            return DatasetEntry(id=track_id, music_metadata=track_metadata, files=track_files)

        with open(self.match_scores_path, 'r') as f:
            match_scores = json.load(f)

        return DatasetIndex(
            version=self.version,
            entries=[build_track_proto(midi_file) for midi_file in self._root_dir.glob('**/*.mid')]
        )
