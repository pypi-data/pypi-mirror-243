from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorIncidents


class GetSegmentIncidents(BaseModel):
    segment_incidents: List["GetSegmentIncidentsSegmentIncidents"] = Field(
        alias="segmentIncidents"
    )


class GetSegmentIncidentsSegmentIncidents(ValidatorIncidents):
    pass


GetSegmentIncidents.model_rebuild()
GetSegmentIncidentsSegmentIncidents.model_rebuild()
