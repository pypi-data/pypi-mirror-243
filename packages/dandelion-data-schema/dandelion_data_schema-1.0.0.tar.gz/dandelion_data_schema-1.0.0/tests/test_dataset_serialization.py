import json
from pathlib import Path

import pydicom
import numpy as np

from dandelion_data_schema.dataset import Record

def test_load_dataset(synthetic_dataset: dict):
    dataset = Record.model_validate(synthetic_dataset)
    assert dataset.age == synthetic_dataset['age']
    assert dataset.sex == synthetic_dataset['sex']
    assert dataset.race == synthetic_dataset['race']
    np.testing.assert_array_equal(dataset.modality_data.waveform, np.array(synthetic_dataset['modality_data']['waveform']).reshape((100, 12)))

    dataset = Record(**synthetic_dataset)
    assert dataset.age == synthetic_dataset['age']

def test_save_dataset_to_json(synthetic_dataset: dict, tmp_path: Path):
    dataset = Record.model_validate(synthetic_dataset)
    dataset_json = dataset.model_dump_json()

    # Save JSON to a temporary file
    file_path = tmp_path / "dataset.json"
    file_path.write_text(dataset_json)

    # Ensure file was saved properly
    assert file_path.exists()

def test_load_dataset_from_json(synthetic_dataset: dict, tmp_path: Path):
    dataset = Record.model_validate(synthetic_dataset)
    file_path = tmp_path / "dataset.json"

    dataset_json = dataset.model_dump_json()
    file_path.write_text(dataset_json)

    # verify the file exists
    assert file_path.exists()
    
    # load the file
    with open(file_path, 'r') as fp:
        dataset_json = json.load(fp)
    dataset = Record.model_validate(dataset_json)

    # verify the data is the same
    assert dataset.age == synthetic_dataset['age']
