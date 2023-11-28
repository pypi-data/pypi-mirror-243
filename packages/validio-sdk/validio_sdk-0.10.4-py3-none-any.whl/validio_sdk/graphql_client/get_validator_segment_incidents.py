from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorIncidents


class GetValidatorSegmentIncidents(BaseModel):
    validator_segment_incidents: List[
        "GetValidatorSegmentIncidentsValidatorSegmentIncidents"
    ] = Field(alias="validatorSegmentIncidents")


class GetValidatorSegmentIncidentsValidatorSegmentIncidents(ValidatorIncidents):
    pass


GetValidatorSegmentIncidents.model_rebuild()
GetValidatorSegmentIncidentsValidatorSegmentIncidents.model_rebuild()
