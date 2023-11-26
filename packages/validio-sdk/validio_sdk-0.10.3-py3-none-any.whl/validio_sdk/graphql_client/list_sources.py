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


class ListSources(BaseModel):
    sources_list: List[
        Annotated[
            Union[
                "ListSourcesSourcesListSource",
                "ListSourcesSourcesListAwsAthenaSource",
                "ListSourcesSourcesListAwsKinesisSource",
                "ListSourcesSourcesListAwsRedshiftSource",
                "ListSourcesSourcesListAwsS3Source",
                "ListSourcesSourcesListDatabricksSource",
                "ListSourcesSourcesListGcpBigQuerySource",
                "ListSourcesSourcesListGcpPubSubLiteSource",
                "ListSourcesSourcesListGcpPubSubSource",
                "ListSourcesSourcesListGcpStorageSource",
                "ListSourcesSourcesListKafkaSource",
                "ListSourcesSourcesListPostgreSqlSource",
                "ListSourcesSourcesListSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourcesList")


class ListSourcesSourcesListSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListSourceCredential"
    windows: List["ListSourcesSourcesListSourceWindows"]
    segmentations: List["ListSourcesSourcesListSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListAwsAthenaSourceCredential"
    windows: List["ListSourcesSourcesListAwsAthenaSourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsAthenaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListAwsAthenaSourceConfig"


class ListSourcesSourcesListAwsAthenaSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsAthenaSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsAthenaSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListAwsKinesisSourceCredential"
    windows: List["ListSourcesSourcesListAwsKinesisSourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsKinesisSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListAwsKinesisSourceConfig"


class ListSourcesSourcesListAwsKinesisSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsKinesisSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsKinesisSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "ListSourcesSourcesListAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListAwsKinesisSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListAwsRedshiftSourceCredential"
    windows: List["ListSourcesSourcesListAwsRedshiftSourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsRedshiftSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListAwsRedshiftSourceConfig"


class ListSourcesSourcesListAwsRedshiftSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsRedshiftSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsRedshiftSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListAwsS3SourceCredential"
    windows: List["ListSourcesSourcesListAwsS3SourceWindows"]
    segmentations: List["ListSourcesSourcesListAwsS3SourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListAwsS3SourceConfig"


class ListSourcesSourcesListAwsS3SourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsS3SourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsS3SourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["ListSourcesSourcesListAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class ListSourcesSourcesListAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class ListSourcesSourcesListDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListDatabricksSourceCredential"
    windows: List["ListSourcesSourcesListDatabricksSourceWindows"]
    segmentations: List["ListSourcesSourcesListDatabricksSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListDatabricksSourceConfig"


class ListSourcesSourcesListDatabricksSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListDatabricksSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListDatabricksSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListDatabricksSourceConfig(BaseModel):
    http_path: str = Field(alias="httpPath")
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListGcpBigQuerySourceCredential"
    windows: List["ListSourcesSourcesListGcpBigQuerySourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpBigQuerySourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListGcpBigQuerySourceConfig"


class ListSourcesSourcesListGcpBigQuerySourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpBigQuerySourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpBigQuerySourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListGcpPubSubLiteSourceCredential"
    windows: List["ListSourcesSourcesListGcpPubSubLiteSourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpPubSubLiteSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListGcpPubSubLiteSourceConfig"


class ListSourcesSourcesListGcpPubSubLiteSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpPubSubLiteSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpPubSubLiteSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "ListSourcesSourcesListGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListGcpPubSubLiteSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListGcpPubSubSourceCredential"
    windows: List["ListSourcesSourcesListGcpPubSubSourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpPubSubSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListGcpPubSubSourceConfig"


class ListSourcesSourcesListGcpPubSubSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpPubSubSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpPubSubSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "ListSourcesSourcesListGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListGcpPubSubSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListGcpStorageSourceCredential"
    windows: List["ListSourcesSourcesListGcpStorageSourceWindows"]
    segmentations: List["ListSourcesSourcesListGcpStorageSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListGcpStorageSourceConfig"


class ListSourcesSourcesListGcpStorageSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpStorageSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpStorageSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional["ListSourcesSourcesListGcpStorageSourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class ListSourcesSourcesListGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class ListSourcesSourcesListKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListKafkaSourceCredential"
    windows: List["ListSourcesSourcesListKafkaSourceWindows"]
    segmentations: List["ListSourcesSourcesListKafkaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListKafkaSourceConfig"


class ListSourcesSourcesListKafkaSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListKafkaSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListKafkaSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional[
        "ListSourcesSourcesListKafkaSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class ListSourcesSourcesListKafkaSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class ListSourcesSourcesListPostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListPostgreSqlSourceCredential"
    windows: List["ListSourcesSourcesListPostgreSqlSourceWindows"]
    segmentations: List["ListSourcesSourcesListPostgreSqlSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListPostgreSqlSourceConfig"


class ListSourcesSourcesListPostgreSqlSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListPostgreSqlSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListPostgreSqlSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListPostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class ListSourcesSourcesListSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "ListSourcesSourcesListSnowflakeSourceCredential"
    windows: List["ListSourcesSourcesListSnowflakeSourceWindows"]
    segmentations: List["ListSourcesSourcesListSnowflakeSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListSourcesSourcesListSnowflakeSourceConfig"


class ListSourcesSourcesListSnowflakeSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListSnowflakeSourceWindows(BaseModel):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListSnowflakeSourceSegmentations(BaseModel):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListSourcesSourcesListSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


ListSources.model_rebuild()
ListSourcesSourcesListSource.model_rebuild()
ListSourcesSourcesListSourceCredential.model_rebuild()
ListSourcesSourcesListSourceWindows.model_rebuild()
ListSourcesSourcesListSourceSegmentations.model_rebuild()
ListSourcesSourcesListAwsAthenaSource.model_rebuild()
ListSourcesSourcesListAwsAthenaSourceCredential.model_rebuild()
ListSourcesSourcesListAwsAthenaSourceWindows.model_rebuild()
ListSourcesSourcesListAwsAthenaSourceSegmentations.model_rebuild()
ListSourcesSourcesListAwsAthenaSourceConfig.model_rebuild()
ListSourcesSourcesListAwsKinesisSource.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceCredential.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceWindows.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceSegmentations.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceConfig.model_rebuild()
ListSourcesSourcesListAwsKinesisSourceConfigMessageFormat.model_rebuild()
ListSourcesSourcesListAwsRedshiftSource.model_rebuild()
ListSourcesSourcesListAwsRedshiftSourceCredential.model_rebuild()
ListSourcesSourcesListAwsRedshiftSourceWindows.model_rebuild()
ListSourcesSourcesListAwsRedshiftSourceSegmentations.model_rebuild()
ListSourcesSourcesListAwsRedshiftSourceConfig.model_rebuild()
ListSourcesSourcesListAwsS3Source.model_rebuild()
ListSourcesSourcesListAwsS3SourceCredential.model_rebuild()
ListSourcesSourcesListAwsS3SourceWindows.model_rebuild()
ListSourcesSourcesListAwsS3SourceSegmentations.model_rebuild()
ListSourcesSourcesListAwsS3SourceConfig.model_rebuild()
ListSourcesSourcesListAwsS3SourceConfigCsv.model_rebuild()
ListSourcesSourcesListDatabricksSource.model_rebuild()
ListSourcesSourcesListDatabricksSourceCredential.model_rebuild()
ListSourcesSourcesListDatabricksSourceWindows.model_rebuild()
ListSourcesSourcesListDatabricksSourceSegmentations.model_rebuild()
ListSourcesSourcesListDatabricksSourceConfig.model_rebuild()
ListSourcesSourcesListGcpBigQuerySource.model_rebuild()
ListSourcesSourcesListGcpBigQuerySourceCredential.model_rebuild()
ListSourcesSourcesListGcpBigQuerySourceWindows.model_rebuild()
ListSourcesSourcesListGcpBigQuerySourceSegmentations.model_rebuild()
ListSourcesSourcesListGcpBigQuerySourceConfig.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSource.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceCredential.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceWindows.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceSegmentations.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceConfig.model_rebuild()
ListSourcesSourcesListGcpPubSubLiteSourceConfigMessageFormat.model_rebuild()
ListSourcesSourcesListGcpPubSubSource.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceCredential.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceWindows.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceSegmentations.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceConfig.model_rebuild()
ListSourcesSourcesListGcpPubSubSourceConfigMessageFormat.model_rebuild()
ListSourcesSourcesListGcpStorageSource.model_rebuild()
ListSourcesSourcesListGcpStorageSourceCredential.model_rebuild()
ListSourcesSourcesListGcpStorageSourceWindows.model_rebuild()
ListSourcesSourcesListGcpStorageSourceSegmentations.model_rebuild()
ListSourcesSourcesListGcpStorageSourceConfig.model_rebuild()
ListSourcesSourcesListGcpStorageSourceConfigCsv.model_rebuild()
ListSourcesSourcesListKafkaSource.model_rebuild()
ListSourcesSourcesListKafkaSourceCredential.model_rebuild()
ListSourcesSourcesListKafkaSourceWindows.model_rebuild()
ListSourcesSourcesListKafkaSourceSegmentations.model_rebuild()
ListSourcesSourcesListKafkaSourceConfig.model_rebuild()
ListSourcesSourcesListKafkaSourceConfigMessageFormat.model_rebuild()
ListSourcesSourcesListPostgreSqlSource.model_rebuild()
ListSourcesSourcesListPostgreSqlSourceCredential.model_rebuild()
ListSourcesSourcesListPostgreSqlSourceWindows.model_rebuild()
ListSourcesSourcesListPostgreSqlSourceSegmentations.model_rebuild()
ListSourcesSourcesListPostgreSqlSourceConfig.model_rebuild()
ListSourcesSourcesListSnowflakeSource.model_rebuild()
ListSourcesSourcesListSnowflakeSourceCredential.model_rebuild()
ListSourcesSourcesListSnowflakeSourceWindows.model_rebuild()
ListSourcesSourcesListSnowflakeSourceSegmentations.model_rebuild()
ListSourcesSourcesListSnowflakeSourceConfig.model_rebuild()
