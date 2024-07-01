import json
import unittest
from pathlib import Path

from google.protobuf.json_format import Parse

from resolv_data import DatasetIndex
from resolv_data.datasets.mir import JSBChoralesDataset
from resolv_data.scripts.import_dataset import import_directory_dataset


class JSBChoralesDatasetTest(unittest.TestCase):

    @property
    def indexes_dir(self) -> Path:
        return Path("./datasets/indexes")

    @property
    def output_dir(self) -> Path:
        return Path("./datasets/output")

    def test_download_and_index(self):
        dataset_modes = JSBChoralesDataset.remote_sources().keys()
        for mode in dataset_modes:
            dataset_root_dir, dataset_index = import_directory_dataset(
                dataset_name='jsb-chorales-v1',
                dataset_mode=mode,
                output_path=self.output_dir,
                temp=False,
                overwrite=True,
                cleanup=True,
                allow_invalid_checksum=False
            )
            self.assertTrue(dataset_root_dir.exists())
            with open(f'{self.indexes_dir}/jsb_chorales_v1_index.json', 'r') as file:
                json_index = json.load(file)
                jsb_chorales_index = Parse(json.dumps(json_index), DatasetIndex())
                self.assertEqual(dataset_index, jsb_chorales_index)


if __name__ == '__main__':
    unittest.main()
