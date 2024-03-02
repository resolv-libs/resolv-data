from pathlib import Path
from typing import Union, Tuple

from ..constants import DATASET_TYPE_MAP
from ..protobuf import DatasetIndex


def import_dataset(dataset_name: str,
                   dataset_mode: str,
                   output_path: Union[str, Path] = None,
                   temp: bool = False,
                   overwrite: bool = False,
                   cleanup: bool = True,
                   allow_invalid_checksum: bool = False) -> Tuple[Path, DatasetIndex]:

    dataset = DATASET_TYPE_MAP[dataset_name](mode=dataset_mode)
    dataset_root_dir = dataset.download(
        output_path=output_path,
        temp=temp,
        overwrite=overwrite,
        cleanup=cleanup,
        allow_invalid_checksum=allow_invalid_checksum
    )
    dataset_index = dataset.compute_index(path_prefix=dataset_root_dir)
    return dataset_root_dir, dataset_index