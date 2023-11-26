from datetime import datetime
from typing import Annotated, Any, List, Literal, Union

from pydantic import Field

from validio_sdk.scalars import SegmentationId, SourceId

from .base_model import BaseModel
from .enums import ComparisonOperator, DecisionBoundsType, NotificationLevel
from .fragments import SegmentDetails


class GetIncidents(BaseModel):
    incidents: List[
        Annotated[
            Union[
                "GetIncidentsIncidentsNotification",
                "GetIncidentsIncidentsSchemaChangeNotification",
                "GetIncidentsIncidentsSegmentLimitExceededNotification",
                "GetIncidentsIncidentsSourceErrorNotification",
                "GetIncidentsIncidentsValidatorThresholdFailureNotification",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetIncidentsIncidentsNotification(BaseModel):
    typename__: Literal["Notification"] = Field(alias="__typename")
    id: Any
    level: NotificationLevel


class GetIncidentsIncidentsSchemaChangeNotification(BaseModel):
    typename__: Literal["SchemaChangeNotification"] = Field(alias="__typename")
    id: Any
    level: NotificationLevel
    created_at: datetime = Field(alias="createdAt")
    payload: Any


class GetIncidentsIncidentsSegmentLimitExceededNotification(BaseModel):
    typename__: Literal["SegmentLimitExceededNotification"] = Field(alias="__typename")
    id: Any
    level: NotificationLevel
    created_at: datetime = Field(alias="createdAt")
    limit: int
    segmentation: "GetIncidentsIncidentsSegmentLimitExceededNotificationSegmentation"


class GetIncidentsIncidentsSegmentLimitExceededNotificationSegmentation(BaseModel):
    id: SegmentationId
    name: str


class GetIncidentsIncidentsSourceErrorNotification(BaseModel):
    typename__: Literal["SourceErrorNotification"] = Field(alias="__typename")
    id: Any
    level: NotificationLevel
    created_at: datetime = Field(alias="createdAt")
    message: str
    source: "GetIncidentsIncidentsSourceErrorNotificationSource"


class GetIncidentsIncidentsSourceErrorNotificationSource(BaseModel):
    id: SourceId
    name: str


class GetIncidentsIncidentsValidatorThresholdFailureNotification(BaseModel):
    typename__: Literal["ValidatorThresholdFailureNotification"] = Field(
        alias="__typename"
    )
    id: Any
    level: NotificationLevel
    segment: "GetIncidentsIncidentsValidatorThresholdFailureNotificationSegment"
    metric: Union[
        "GetIncidentsIncidentsValidatorThresholdFailureNotificationMetricValidatorMetric",
        "GetIncidentsIncidentsValidatorThresholdFailureNotificationMetricValidatorMetricWithDynamicThreshold",
        "GetIncidentsIncidentsValidatorThresholdFailureNotificationMetricValidatorMetricWithFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentsIncidentsValidatorThresholdFailureNotificationSegment(SegmentDetails):
    pass


class GetIncidentsIncidentsValidatorThresholdFailureNotificationMetricValidatorMetric(
    BaseModel
):
    typename__: Literal["ValidatorMetric"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    deviation: float


class GetIncidentsIncidentsValidatorThresholdFailureNotificationMetricValidatorMetricWithDynamicThreshold(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithDynamicThreshold"] = Field(
        alias="__typename"
    )
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    deviation: float
    lower_bound: float = Field(alias="lowerBound")
    upper_bound: float = Field(alias="upperBound")
    decision_bounds_type: DecisionBoundsType = Field(alias="decisionBoundsType")
    is_burn_in: bool = Field(alias="isBurnIn")


class GetIncidentsIncidentsValidatorThresholdFailureNotificationMetricValidatorMetricWithFixedThreshold(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithFixedThreshold"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    deviation: float
    operator: ComparisonOperator
    bound: float


GetIncidents.model_rebuild()
GetIncidentsIncidentsNotification.model_rebuild()
GetIncidentsIncidentsSchemaChangeNotification.model_rebuild()
GetIncidentsIncidentsSegmentLimitExceededNotification.model_rebuild()
GetIncidentsIncidentsSegmentLimitExceededNotificationSegmentation.model_rebuild()
GetIncidentsIncidentsSourceErrorNotification.model_rebuild()
GetIncidentsIncidentsSourceErrorNotificationSource.model_rebuild()
GetIncidentsIncidentsValidatorThresholdFailureNotification.model_rebuild()
GetIncidentsIncidentsValidatorThresholdFailureNotificationSegment.model_rebuild()
GetIncidentsIncidentsValidatorThresholdFailureNotificationMetricValidatorMetric.model_rebuild()
GetIncidentsIncidentsValidatorThresholdFailureNotificationMetricValidatorMetricWithDynamicThreshold.model_rebuild()
GetIncidentsIncidentsValidatorThresholdFailureNotificationMetricValidatorMetricWithFixedThreshold.model_rebuild()
