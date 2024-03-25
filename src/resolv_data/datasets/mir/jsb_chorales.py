"""
Module Name: jsb_chorales.py.
Description: JSB Chorales Dataset.
Author: Matteo Pettenò.
Copyright (c) 2024, Matteo Pettenò
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""
from pathlib import Path
from typing import Dict, List, Union

from resolv_data import utilities
from resolv_data.base import DatasetInfo, RemoteSource, DirectoryDataset
from resolv_data.protobuf import DatasetIndex, DatasetEntry, EntryFile

_NAME = "JSB Chorales"

_DESCRIPTION = """\
The JSB Chorales Dataset is a collection of 382 four-part chorales by Johann \
Sebastian Bach. This dataset is used in the paper "Modeling Temporal \
Dependencies in High-Dimensional Sequences: Application to Polyphonic Music \
Generation and Transcription" in ICML 2012. It comes with train, test and \
validation split used in the paper "Harmonising Chorales by Probabilistic \
Inference" in NIPS 2005."""

_HOMEPAGE = "https://arxiv.org/pdf/2107.10388v4.pdf"

_CITATION = """\
@inproceedings{boulangerlewandowski2012modeling,
  author={Nicolas Boulanger-Lewandowski and Yoshua Bengio and Pascal Vincent},
  title={Modeling Temporal Dependencies in High-Dimensional Sequences: Application to Polyphonic Music Generation and Transcription},
  booktitle={Proceedings of the 29th International Conference on Machine Learning (ICML)},
  year=2012
}"""

_LICENSE_INFO = ""


class JSBChoralesDataset(DirectoryDataset):

    @staticmethod
    def remote_sources() -> Dict[str, List[RemoteSource]]:
        return {
            "full": [
                RemoteSource(
                    filename="jsb_chorales.zip",
                    url="https://drive.google.com/uc?id=1ryA77ynWH1eiUTn7tNfuvhGWmo88B1Zf&export=download",
                    checksum="6425acfc5a1191d11482ed50eb5f5edc0c9c24555a10cd3f81f6d54925c9d2a7",
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

    def _compute_index_internal(self, path_prefix: Union[str, Path]) -> DatasetIndex:

        def build_track_proto(musicxml_file):
            track_id = musicxml_file.stem
            track_files = {
                'mxml': EntryFile(path=f'{str(path_prefix)}/{str(musicxml_file.relative_to(self._root_dir))}',
                                  md5_checksum=utilities.compute_checksum(musicxml_file, checksum_type='md5'))
            }
            return DatasetEntry(id=track_id, files=track_files)

        path_prefix = path_prefix if path_prefix is not None else self._root_dir
        musicxml_files = []
        for ext in ('*.mxml', '*.mxl'):
            musicxml_files.extend(self._root_dir.glob(f'**/{ext}'))
        return DatasetIndex(
            id=self.root_dir_name,
            version=self.version,
            entries=[build_track_proto(musicxml_file) for musicxml_file in musicxml_files]
        )
