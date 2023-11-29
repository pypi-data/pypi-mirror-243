import json
import pytest
import numpy as np
from pydantic import ValidationError
from dandelion_data_schema.output import ModelOutput

def test_successful_creation_with_percentage_prediction():
    model = ModelOutput(prediction_percentage=50.5)
    assert model.prediction_percentage == 50.5

def test_successful_creation_with_continuous_prediction():
    model = ModelOutput(prediction_continuous=123.456) 
    assert model.prediction_continuous == 123.456

def test_successful_creation_with_binary_prediction():
    model = ModelOutput(prediction_binary=1.0)
    assert model.prediction_binary == 1.0

def test_successful_creation_with_multilabel_prediction():
    multilabel_prediction = np.array([0.1, 0.9])
    model = ModelOutput(prediction_multilabel=multilabel_prediction)
    assert np.array_equal(model.prediction_multilabel, multilabel_prediction)

def test_successful_creation_with_multiclass_prediction():
    multiclass_prediction = np.array([0.2, 0.3, 0.5])
    model = ModelOutput(prediction_multiclass=multiclass_prediction)
    assert np.array_equal(model.prediction_multiclass, multiclass_prediction)

def test_validation_error_with_no_prediction():
    with pytest.raises(ValidationError) as exc_info:
        ModelOutput()  # No predictions provided
    assert 'at least one prediction must be provided' in str(exc_info.value)

@pytest.mark.parametrize("prediction_field, value", [
    ("prediction_percentage", None),
    ("prediction_continuous", None),
    ("prediction_binary", None),
    ("prediction_multilabel", None),
    ("prediction_multiclass", None),
])
def test_missing_individual_predictions_do_not_raise_errors(prediction_field, value):
    # All individual predictions are optional; missing ones should not cause errors as long as at least one is provided
    prediction_fields = {
        "prediction_percentage": 50.0,
        "prediction_continuous": 123.456,
        "prediction_binary": 0.0,
        "prediction_multilabel": np.array([0.1, 0.9]),
        "prediction_multiclass": np.array([0.1, 0.2, 0.7]),
    }
    prediction_fields[prediction_field] = value
    model = ModelOutput(**prediction_fields)
    assert getattr(model, prediction_field) is value

def test_model_output_serialization_to_dict():
    multilabel_prediction = np.array([0.1, 0.9])
    model = ModelOutput(prediction_multilabel=multilabel_prediction)
    model_data = model.model_dump()
    assert 'prediction_multilabel' in model_data
    assert model_data['prediction_multilabel'][0] == multilabel_prediction[0]

def test_model_output_serialization_to_json():
    multiclass_prediction = np.array([0.2, 0.3, 0.5])
    model = ModelOutput(prediction_multiclass=multiclass_prediction)
    model_json = model.model_dump_json()
    # The JSON output should be a string
    assert isinstance(model_json, str)
    # Convert back to a Python dict to check for expected data
    json_data = json.loads(model_json)
    # Check important keys and values
    assert 'prediction_multiclass' in json_data
    assert json_data['prediction_multiclass'][0] == multiclass_prediction[0]
