from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import (
    CredentialId,
    CronExpression,
    JsonTypeDefinition,
    SegmentationId,
    SourceId,
    WindowId,
)

from .base_model import BaseModel
from .enums import FileFormat, SourceState, StreamingSourceMessageFormat


class GetSourceByResourceName(BaseModel):
    source_by_resource_name: Optional[
        Annotated[
            Union[
                "GetSourceByResourceNameSourceByResourceNameSource",
                "GetSourceByResourceNameSourceByResourceNameAwsAthenaSource",
                "GetSourceByResourceNameSourceByResourceNameAwsKinesisSource",
                "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSource",
                "GetSourceByResourceNameSourceByResourceNameAwsS3Source",
                "GetSourceByResourceNameSourceByResourceNameDatabricksSource",
                "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySource",
                "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSource",
                "GetSourceByResourceNameSourceByResourceNameGcpPubSubSource",
                "GetSourceByResourceNameSourceByResourceNameGcpStorageSource",
                "GetSourceByResourceNameSourceByResourceNameKafkaSource",
                "GetSourceByResourceNameSourceByResourceNamePostgreSqlSource",
                "GetSourceByResourceNameSourceByResourceNameSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceByResourceName")


class GetSourceByResourceNameSourceByResourceNameSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceConfig"


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfig"


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceConfig"


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameAwsS3SourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameAwsS3SourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameAwsS3SourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfig"


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceByResourceNameSourceByResourceNameDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameDatabricksSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameDatabricksSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameDatabricksSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameDatabricksSourceConfig"


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameDatabricksSourceConfig(BaseModel):
    http_path: str = Field(alias="httpPath")
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceConfig"


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCredential"
    windows: List[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceWindows"
    ]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfig"


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCredential(
    BaseModel
):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfig"


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameSourceByResourceNameGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameGcpStorageSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfig"


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional[
        "GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfigCsv"
    ]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceByResourceNameSourceByResourceNameKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameKafkaSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameKafkaSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameKafkaSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameKafkaSourceConfig"


class GetSourceByResourceNameSourceByResourceNameKafkaSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameKafkaSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameKafkaSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional[
        "GetSourceByResourceNameSourceByResourceNameKafkaSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceByResourceNameSourceByResourceNameKafkaSourceConfigMessageFormat(
    BaseModel
):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceConfig"


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceByResourceNameSourceByResourceNameSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCredential"
    windows: List["GetSourceByResourceNameSourceByResourceNameSnowflakeSourceWindows"]
    segmentations: List[
        "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceSegmentations"
    ]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetSourceByResourceNameSourceByResourceNameSnowflakeSourceConfig"


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceSegmentations(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceByResourceNameSourceByResourceNameSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


GetSourceByResourceName.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsAthenaSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsKinesisSourceConfigMessageFormat.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsRedshiftSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3Source.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameAwsS3SourceConfigCsv.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameDatabricksSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpBigQuerySourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubLiteSourceConfigMessageFormat.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpPubSubSourceConfigMessageFormat.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameGcpStorageSourceConfigCsv.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameKafkaSourceConfigMessageFormat.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNamePostgreSqlSourceConfig.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSource.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSourceCredential.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSourceWindows.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSourceSegmentations.model_rebuild()
GetSourceByResourceNameSourceByResourceNameSnowflakeSourceConfig.model_rebuild()
