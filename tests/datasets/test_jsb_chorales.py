import json
import unittest

from google.protobuf.json_format import Parse

from resolv_data import DatasetIndex
from resolv_data.datasets.mir import JSBChoralesDataset
from resolv_data.scripts.import_dataset import import_dataset

INDEXES_DIR = "./indexes"
OUTPUT_DIR = "./output"


class JSBChoralesDatasetTest(unittest.TestCase):

    def test_download_and_index(self):
        dataset_modes = JSBChoralesDataset.remote_sources().keys()
        for mode in dataset_modes:
            dataset_root_dir, dataset_index = import_dataset(
                dataset_name='jsb-chorales-v1',
                dataset_mode=mode,
                output_path=OUTPUT_DIR,
                temp=False,
                overwrite=True,
                cleanup=True,
                allow_invalid_checksum=False
            )
            self.assertTrue(dataset_root_dir.exists())
            with open(f'{INDEXES_DIR}/jsb_chorales_v1_index.json', 'r') as file:
                json_index = json.load(file)
                jsb_chorales_index = Parse(json.dumps(json_index), DatasetIndex())
                self.assertEqual(dataset_index, jsb_chorales_index)


if __name__ == '__main__':
    unittest.main()
