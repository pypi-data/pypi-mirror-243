
from enum import Enum
from typing import Dict, List, Optional, Union
from datetime import datetime

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from .lab import Lab, LabName
from .report import Report
from .study import ImagingStudy, WaveformStudy


class ModalityType(str, Enum):
    waveform = "waveform"
    dicom = "dicom"

class SexEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class RaceEnum(str, Enum):
    white = "White"
    black = "Black or African American"
    asian = "Asian American or Pacific Islander"
    native = "American Indian or Native Alaskan"

class EthnicityEnum(str, Enum):
    hispanic = "Hispanic"
    non_hispanic = "Non-Hispanic"

class Record(BaseModel):
    model_config = ConfigDict(
        json_encoders = {
            np.ndarray: lambda v: v.tolist(),
        },
    )
    schema_version: str = '1.0.0'
    record_name: str
    age: Optional[float] = Field(..., ge=0, description='Age in years')
    sex: Optional[SexEnum]
    race: Optional[RaceEnum]
    ethnicity: Optional[EthnicityEnum]
    height: Optional[float] = Field(..., ge=0, description='Height in centimeters')
    weight: Optional[float] = Field(..., ge=0, description='Weight in kilograms')

    # diagnosis codes
    icd10: Optional[List[str]] = Field(None, alias='icd10')
    
    # modality data
    modality_type: ModalityType
    modality_data: Union[WaveformStudy, ImagingStudy]
    modality_report: Optional[Report] = Field(None, alias='report')

    # other modality information which may also be collected
    related_ecg: Optional[List[WaveformStudy]] = Field(None, alias='ecg')
    related_ct: Optional[List[ImagingStudy]] = Field(None, alias='ct')
    related_echo: Optional[List[ImagingStudy]] = Field(None, alias='echo')

    # lab data
    related_lab: Optional[Dict[LabName, Lab]] = Field(None, alias='lab')
