"""
Module Name: maestro.py.
Description: MAESTRO Dataset.
Author: Matteo Pettenò.
Copyright (c) 2024, Matteo Pettenò
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""
import json
from abc import ABC
from pathlib import Path
from typing import Dict, List, Union

from resolv_data import utilities
from resolv_data.base import DatasetInfo, DirectoryDataset, RemoteSource
from resolv_data.protobuf import DatasetIndex, DatasetEntry, EntryFile

_NAME = "MAESTRO"

_DESCRIPTION = """\
MAESTRO (MIDI and Audio Edited for Synchronous TRacks and Organization) is a \
dataset composed of over 200 hours of virtuosic piano performances captured \
with fine alignment (~3 ms) between note labels and audio waveforms."""

_HOMEPAGE = "https://magenta.tensorflow.org/datasets/maestro"

_LICENSE_INFO = "Creative Commons Attribution Non-Commercial Share-Alike 4.0 (CC BY-NC-SA 4.0)."

_CITATION = """\
@inproceedings{hawthorne2018enabling,
  title={Enabling Factorized Piano Music Modeling and Generation with the {MAESTRO} Dataset},
  author={Curtis Hawthorne and Andriy Stasyuk and Adam Roberts and Ian Simon and Cheng-Zhi Anna Huang and Sander \
  Dieleman and Erich Elsen and Jesse Engel and Douglas Eck},
  booktitle={Proceedings of the 7th International Conference on Learning Representations (ICLR)},
  year=2019,
  url={https://openreview.net/forum?id=r1lYRjC9F7}
}"""


class MAESTRODataset(DirectoryDataset, ABC):

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
    def metadata_path(self) -> Path:
        return self._root_dir / f'maestro-v{self.version}.json'

    def _compute_index_internal(self, path_prefix: Union[str, Path]) -> DatasetIndex:
        def build_track_proto(track_metadata):
            track_files = {}
            midi_filepath_check = str(self._root_dir / track_metadata['midi_filename'])
            track_files['midi'] = EntryFile(
                path=f"{str(path_prefix)}/{track_metadata['midi_filename']}",
                md5_checksum=utilities.compute_checksum(midi_filepath_check, checksum_type='md5')
            )
            if self._mode == 'full':
                audio_filepath_check = str(self._root_dir / track_metadata['audio_filename'])
                track_files['audio'] = EntryFile(
                    path=f"{str(path_prefix)}/{track_metadata['audio_filename']}",
                    md5_checksum=utilities.compute_checksum(audio_filepath_check, checksum_type='md5')
                )
            metadata = DatasetEntry.MusicTrackMetadata(
                composer=track_metadata['canonical_composer'],
                title=track_metadata['canonical_title'],
                year=track_metadata['year'],
                duration=track_metadata['duration']
            )
            return DatasetEntry(
                id=track_metadata['midi_filename'].split('.')[0],
                music_metadata=metadata,
                files=track_files,
                split=track_metadata['split']
            )

        metadata_content = self.metadata_path.read_text(encoding="UTF-8")
        maestro_metadata = json.loads(metadata_content)
        path_prefix = Path(path_prefix) if path_prefix is not None else self._root_dir
        return DatasetIndex(
            id=self.root_dir_name,
            version=self.version,
            entries=[build_track_proto(row) for i, row in enumerate(maestro_metadata)]
        )


class MAESTRODatasetV1(MAESTRODataset):
    """MAESTRO Dataset V1."""

    @staticmethod
    def remote_sources() -> Dict[str, List[RemoteSource]]:
        return {
            "full": [
                RemoteSource(
                    filename="maestro-v1.0.0.zip",
                    url="https://storage.googleapis.com/magentadata/datasets/maestro/v1.0.0/maestro-v1.0.0.zip",
                    checksum="97471232457147d5bffa72db8c4897166ba52afd4a64197004b806c2ec85ad27",
                    checksum_type="sha256",
                    main_source=True,
                    archive=True,
                    has_archived_root=True
                )],
            "midi": [
                RemoteSource(
                    filename="maestro-v1.0.0-midi.zip",
                    url="https://storage.googleapis.com/magentadata/datasets/maestro/v1.0.0/maestro-v1.0.0-midi.zip",
                    checksum="f620f9e1eceaab8beea10617599add2e9c83234199b550382a2f603098ae7135",
                    checksum_type="sha256",
                    main_source=True,
                    archive=True,
                    has_archived_root=True
                )]
        }

    @property
    def version(self) -> str:
        return "1.0.0"


class MAESTRODatasetV2(MAESTRODataset):
    """MAESTRO Dataset V2."""

    @staticmethod
    def remote_sources() -> Dict[str, List[RemoteSource]]:
        return {
            "full": [
                RemoteSource(
                    filename="maestro-v2.0.0.zip",
                    url="https://storage.googleapis.com/magentadata/datasets/maestro/v2.0.0/maestro-v2.0.0.zip",
                    checksum="572c6054e8d2c7219aa4df9a29357da0f9789524c11fa38cef7d4bd8542c93f0",
                    checksum_type="sha256",
                    main_source=True,
                    archive=True,
                    has_archived_root=True
                )],
            "midi": [
                RemoteSource(
                    filename="maestro-v2.0.0-midi.zip",
                    url="https://storage.googleapis.com/magentadata/datasets/maestro/v2.0.0/maestro-v2.0.0-midi.zip",
                    checksum="ec2cc9d94886c6b376db1eaa2b8ad1ce62ff9f0a28b3744782b13163295dadf3",
                    checksum_type="sha256",
                    main_source=True,
                    archive=True,
                    has_archived_root=True
                )]
        }

    @property
    def version(self) -> str:
        return "2.0.0"


class MAESTRODatasetV3(MAESTRODataset):
    """MAESTRO Dataset V3."""

    @staticmethod
    def remote_sources() -> Dict[str, List[RemoteSource]]:
        return {
            "full": [
                RemoteSource(
                    filename="maestro-v3.0.0.zip",
                    url="https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0.zip",
                    checksum="6680fea5be2339ea15091a249fbd70e49551246ddbd5ca50f1b2352c08c95291",
                    checksum_type="sha256",
                    main_source=True,
                    archive=True,
                    has_archived_root=True
                )],
            "midi": [
                RemoteSource(
                    filename="maestro-v3.0.0-midi.zip",
                    url="https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip",
                    checksum="70470ee253295c8d2c71e6d9d4a815189e35c89624b76d22fce5a019d5dde12c",
                    checksum_type="sha256",
                    main_source=True,
                    archive=True,
                    has_archived_root=True
                )]
        }

    @property
    def version(self) -> str:
        return "3.0.0"

    def _compute_index_internal(self, path_prefix: Union[str, Path]) -> DatasetIndex:
        def build_track_proto(track_idx):
            track_files = {}
            midi_filepath_check = str(self._root_dir / maestro_metadata['midi_filename'][str(track_idx)])
            track_files['midi'] = EntryFile(
                path=f"{path_prefix}/{maestro_metadata['midi_filename'][str(track_idx)]}",
                md5_checksum=utilities.compute_checksum(midi_filepath_check, checksum_type='md5')
            )
            if self._mode == 'full':
                audio_filepath_check = str(self._root_dir / maestro_metadata['audio_filename'][str(track_idx)])
                track_files['audio'] = EntryFile(
                    path=f"{str(path_prefix)}/{maestro_metadata['audio_filename'][str(track_idx)]}",
                    md5_checksum=utilities.compute_checksum(audio_filepath_check, checksum_type='md5')
                )
            track_metadata = DatasetEntry.MusicTrackMetadata(
                composer=maestro_metadata['canonical_composer'][str(track_idx)],
                title=maestro_metadata['canonical_title'][str(track_idx)],
                year=maestro_metadata['year'][str(track_idx)],
                duration=maestro_metadata['duration'][str(track_idx)]
            )
            return DatasetEntry(
                id=maestro_metadata['midi_filename'][str(track_idx)].split('.')[0],
                music_metadata=track_metadata,
                files=track_files,
                split=maestro_metadata['split'][str(track_idx)],
            )

        metadata_content = self.metadata_path.read_text(encoding="UTF-8")
        maestro_metadata = json.loads(metadata_content)
        path_prefix = path_prefix if path_prefix is not None else self._root_dir
        return DatasetIndex(
            id=self.root_dir_name,
            version=self.version,
            entries=[build_track_proto(i) for i, _ in enumerate(maestro_metadata['midi_filename'])]
        )
