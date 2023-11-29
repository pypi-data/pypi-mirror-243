from dataclasses import dataclass
from enum import Enum
from whylogs.core.schema import DatasetSchema
from typing import Optional


class DatasetCadence(Enum):
    HOURLY = "HOURLY"
    DAILY = "DAILY"


class DatasetUploadCadenceGranularity(Enum):
    MINUTE = "M"
    HOUR = "H"
    DAY = "D"


@dataclass
class DatasetUploadCadence:
    interval: int
    granularity: DatasetUploadCadenceGranularity


@dataclass
class DatasetOptions:
    schema: Optional[DatasetSchema]
    dataset_cadence: DatasetCadence
    whylabs_upload_cadence: DatasetUploadCadence
