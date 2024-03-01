""" This module contains constants relative to the datasets. """
from typing import Dict, Type

import resolv_data.datasets as datasets
from resolv_data.base import DirectoryDataset

# Dictionary mapping dataset names to their respective classes
DATASET_TYPE_MAP: Dict[str, Type[DirectoryDataset]] = {
    'maestro-v3': datasets.mir.MAESTRODatasetV3,
    'maestro-v2': datasets.mir.MAESTRODatasetV2,
    'maestro-v1': datasets.mir.MAESTRODatasetV1,
    'lakh-midi-v1': datasets.mir.LakhMIDIDatasetV1,
    'jsb-chorales-v1': datasets.mir.JSBChoralesDataset
}


def get_dataset_root_dir_name(dataset_name: str, dataset_mode: str) -> str:
    """ Retrieves the root directory name of a dataset.

    Args:
        dataset_name (str): The name of the dataset.
        dataset_mode (str): The mode of the dataset.

    Returns:
        (str): The root directory name of the dataset.

    Raises:
        KeyError: If the specified dataset name is not found in the DATASET_TYPE_MAP.
    """
    dataset = DATASET_TYPE_MAP[dataset_name](mode=dataset_mode)
    return dataset.root_dir_name
