from datetime import datetime
from typing import Annotated, Any, List, Literal, Union

from pydantic import Field

from validio_sdk.scalars import SegmentationId

from .base_model import BaseModel
from .enums import NotificationLevel


class GetSourceIncidents(BaseModel):
    source_incidents: List[
        Annotated[
            Union[
                "GetSourceIncidentsSourceIncidentsSchemaChangeNotification",
                "GetSourceIncidentsSourceIncidentsSegmentLimitExceededNotification",
                "GetSourceIncidentsSourceIncidentsSourceErrorNotification",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceIncidents")


class GetSourceIncidentsSourceIncidentsSchemaChangeNotification(BaseModel):
    typename__: Literal["SchemaChangeNotification"] = Field(alias="__typename")
    id: Any
    level: NotificationLevel
    created_at: datetime = Field(alias="createdAt")
    payload: Any


class GetSourceIncidentsSourceIncidentsSegmentLimitExceededNotification(BaseModel):
    typename__: Literal["SegmentLimitExceededNotification"] = Field(alias="__typename")
    id: Any
    level: NotificationLevel
    created_at: datetime = Field(alias="createdAt")
    limit: int
    segmentation: "GetSourceIncidentsSourceIncidentsSegmentLimitExceededNotificationSegmentation"


class GetSourceIncidentsSourceIncidentsSegmentLimitExceededNotificationSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str


class GetSourceIncidentsSourceIncidentsSourceErrorNotification(BaseModel):
    typename__: Literal["SourceErrorNotification"] = Field(alias="__typename")


GetSourceIncidents.model_rebuild()
GetSourceIncidentsSourceIncidentsSchemaChangeNotification.model_rebuild()
GetSourceIncidentsSourceIncidentsSegmentLimitExceededNotification.model_rebuild()
GetSourceIncidentsSourceIncidentsSegmentLimitExceededNotificationSegmentation.model_rebuild()
GetSourceIncidentsSourceIncidentsSourceErrorNotification.model_rebuild()
