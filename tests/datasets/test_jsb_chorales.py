import json
import unittest
from pathlib import Path

from google.protobuf.json_format import Parse

from resolv_data.datasets.mir import JSBChoralesDataset
from resolv_data.protobuf.protos.dataset_index_pb2 import DatasetIndex

INDEXES_DIR = "./indexes"
OUTPUT_DIR = "./output"


class JSBChoralesDatasetTest(unittest.TestCase):

    def test_download_and_index(self):
        dataset_modes = JSBChoralesDataset.remote_sources().keys()
        for mode in dataset_modes:
            dataset = JSBChoralesDataset(mode=mode)
            dataset_root_dir = dataset.download(
                output_path=OUTPUT_DIR,
                temp=False,
                overwrite=True,
                cleanup=True,
                allow_invalid_checksum=False
            )
            self.assertEqual(dataset_root_dir, Path(f'{OUTPUT_DIR}/{dataset.root_dir_name}'))
            dataset_index = dataset.compute_index(path_prefix=dataset_root_dir)
            with open(f'{INDEXES_DIR}/jsb_chorales_index.json', 'r') as file:
                json_index = json.load(file)
                jsb_chorales_index = Parse(json.dumps(json_index), DatasetIndex())
                self.assertEqual(dataset_index, jsb_chorales_index)


if __name__ == '__main__':
    unittest.main()
