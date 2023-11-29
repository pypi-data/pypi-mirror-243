from enum import Enum
from typing import Dict, List, Optional, Union

import numpy as np
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator, validator

from .lab import Lab, LabName


class ModelOutput(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders = {
            np.ndarray: lambda v: v.tolist(),
        },
    )
    schema_version: str = '1.0.0'
    prediction_percentage: Optional[float] = None
    prediction_continuous: Optional[float] = None
    prediction_binary: Optional[float] = None
    prediction_multilabel: Optional[np.ndarray] = None
    prediction_multiclass: Optional[np.ndarray] = None

    @model_validator(mode='after')
    def validate_at_least_one_prediction_exists(self) -> 'ModelOutput':
        # dynamically get field names beginning with prediction_
        prediction_fields = [field for field in self.model_fields if field.startswith('prediction_')]

        missing_prediction = True
        for field in prediction_fields:
            if getattr(self, field) is not None:
                missing_prediction = False
                break
        
        if missing_prediction:
            raise ValueError('at least one prediction must be provided')
        return self
