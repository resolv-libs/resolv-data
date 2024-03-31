""" TODO - module doc """
from pathlib import Path
from typing import Union, Tuple

from ..constants import DATASET_TYPE_MAP
from ..protobuf import DatasetIndex


def import_directory_dataset(dataset_name: str,
                             dataset_mode: str,
                             output_path: Union[str, Path] = None,
                             index_path_prefix: str = None,
                             temp: bool = False,
                             overwrite: bool = False,
                             cleanup: bool = True,
                             allow_invalid_checksum: bool = False) -> Tuple[Path, DatasetIndex]:
    """ TODO - function doc """
    dataset = DATASET_TYPE_MAP[dataset_name](mode=dataset_mode)
    dataset_root_dir = dataset.download(
        output_path=output_path,
        temp=temp,
        overwrite=overwrite,
        cleanup=cleanup,
        allow_invalid_checksum=allow_invalid_checksum
    )
    dataset_index = dataset.compute_index(path_prefix=index_path_prefix if index_path_prefix else dataset_root_dir)
    return dataset_root_dir, dataset_index
