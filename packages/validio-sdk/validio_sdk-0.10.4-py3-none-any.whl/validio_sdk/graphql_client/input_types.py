from datetime import datetime
from typing import Annotated, Any, List, Optional

from pydantic import Field, PlainSerializer

from validio_sdk.scalars import (
    CredentialId,
    CronExpression,
    JsonFilterExpression,
    JsonPointer,
    JsonTypeDefinition,
    SegmentationId,
    SourceId,
    ValidatorId,
    WindowId,
    serialize_json_filter_expression,
    serialize_rfc3339_datetime,
)

from .base_model import BaseModel
from .enums import (
    CategoricalDistributionMetric,
    ComparisonOperator,
    DecisionBoundsType,
    FileFormat,
    NotificationTypename,
    NumericAnomalyMetric,
    NumericDistributionMetric,
    NumericMetric,
    RelativeTimeMetric,
    RelativeVolumeMetric,
    Role,
    StreamingSourceMessageFormat,
    UserStatus,
    VolumeMetric,
    WindowTimeUnit,
)


class AwsAthenaCredentialCreateInput(BaseModel):
    access_key: str = Field(alias="accessKey")
    name: str
    query_result_location: str = Field(alias="queryResultLocation")
    region: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    secret_key: str = Field(alias="secretKey")


class AwsAthenaCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    secret_key: str = Field(alias="secretKey")


class AwsAthenaCredentialUpdateInput(BaseModel):
    access_key: str = Field(alias="accessKey")
    id: CredentialId
    query_result_location: str = Field(alias="queryResultLocation")
    region: str
    secret_key: str = Field(alias="secretKey")


class AwsAthenaInferSchemaInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    database: str
    table: str


class AwsAthenaSourceCreateInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: str
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    table: str


class AwsAthenaSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression] = None


class AwsCredentialCreateInput(BaseModel):
    access_key: str = Field(alias="accessKey")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    secret_key: str = Field(alias="secretKey")


class AwsCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    secret_key: str = Field(alias="secretKey")


class AwsCredentialUpdateInput(BaseModel):
    access_key: str = Field(alias="accessKey")
    id: CredentialId
    secret_key: str = Field(alias="secretKey")


class AwsKinesisInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    region: str
    stream_name: str = Field(alias="streamName")


class AwsKinesisSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: str
    region: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    stream_name: str = Field(alias="streamName")


class AwsKinesisSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )


class AwsRedshiftCredentialCreateInput(BaseModel):
    default_database: str = Field(alias="defaultDatabase")
    host: str
    name: str
    password: str
    port: int
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    user: str


class AwsRedshiftCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class AwsRedshiftCredentialUpdateInput(BaseModel):
    default_database: str = Field(alias="defaultDatabase")
    host: str
    id: CredentialId
    password: str
    port: int
    user: str


class AwsRedshiftInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    database: Optional[str] = None
    db_schema: str = Field(alias="schema")
    table: str


class AwsRedshiftSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: Optional[str] = None
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    db_schema: str = Field(alias="schema")
    table: str


class AwsRedshiftSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression] = None


class AwsS3InferSchemaInput(BaseModel):
    bucket: str
    credential_id: CredentialId = Field(alias="credentialId")
    csv: Optional["CsvParserInput"] = None
    file_format: Optional[FileFormat] = Field(alias="fileFormat", default=None)
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    prefix: str


class AwsS3SourceCreateInput(BaseModel):
    bucket: str
    credential_id: CredentialId = Field(alias="credentialId")
    csv: Optional["CsvParserInput"] = None
    file_format: Optional[FileFormat] = Field(alias="fileFormat", default=None)
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    name: str
    prefix: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None


class AwsS3SourceUpdateInput(BaseModel):
    csv: Optional["CsvParserInput"] = None
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    schedule: Optional[CronExpression] = None


class CategoricalDistributionValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: CategoricalDistributionMetric
    name: Optional[str] = None
    reference_source_config: "ReferenceSourceConfigCreateInput" = Field(
        alias="referenceSourceConfig"
    )
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: JsonPointer = Field(alias="sourceField")


class CategoricalDistributionValidatorUpdateInput(BaseModel):
    id: ValidatorId
    reference_source_config: "ReferenceSourceConfigUpdateInput" = Field(
        alias="referenceSourceConfig"
    )
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class ChannelDeleteInput(BaseModel):
    id: Any


class CsvParserInput(BaseModel):
    delimiter: str
    null_marker: Optional[str] = Field(alias="nullMarker", default=None)


class DatabricksCredentialCreateInput(BaseModel):
    access_token: str = Field(alias="accessToken")
    host: str
    name: str
    port: int
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class DatabricksCredentialSecretChangedInput(BaseModel):
    access_token: str = Field(alias="accessToken")
    id: CredentialId


class DatabricksCredentialUpdateInput(BaseModel):
    access_token: str = Field(alias="accessToken")
    host: str
    id: CredentialId
    port: int


class DatabricksInferSchemaInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    http_path: str = Field(alias="httpPath")
    db_schema: str = Field(alias="schema")
    table: str


class DatabricksListCatalogsInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    http_path: str = Field(alias="httpPath")


class DatabricksListSchemasInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    http_path: str = Field(alias="httpPath")


class DatabricksListTablesInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    http_path: str = Field(alias="httpPath")
    db_schema: str = Field(alias="schema")


class DatabricksListWarehousesInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")


class DatabricksSourceCreateInput(BaseModel):
    catalog: str
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    http_path: str = Field(alias="httpPath")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    db_schema: str = Field(alias="schema")
    table: str


class DatabricksSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression] = None


class DbtArtifactUploadInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    manifest: Any
    run_results: Optional[Any] = Field(alias="runResults", default=None)


class DemoCredentialCreateInput(BaseModel):
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class DemoSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class DynamicThresholdCreateInput(BaseModel):
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType", default=None
    )
    sensitivity: float


class FileWindowCreateInput(BaseModel):
    data_time_field: JsonPointer = Field(alias="dataTimeField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_id: SourceId = Field(alias="sourceId")


class FixedBatchWindowCreateInput(BaseModel):
    batch_size: int = Field(alias="batchSize")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs", default=None)
    data_time_field: JsonPointer = Field(alias="dataTimeField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    segmented_batching: bool = Field(alias="segmentedBatching")
    source_id: SourceId = Field(alias="sourceId")


class FixedBatchWindowUpdateInput(BaseModel):
    batch_size: int = Field(alias="batchSize")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs", default=None)
    id: WindowId
    segmented_batching: bool = Field(alias="segmentedBatching")


class FixedThresholdCreateInput(BaseModel):
    operator: ComparisonOperator
    value: float


class FreshnessValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    name: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")


class FreshnessValidatorUpdateInput(BaseModel):
    id: ValidatorId
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class GcpBigQueryInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    dataset: str
    project: str
    table: str


class GcpBigQuerySourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    dataset: str
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    project: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    table: str


class GcpBigQuerySourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression] = None


class GcpCredentialCreateInput(BaseModel):
    credential: str
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class GcpCredentialSecretChangedInput(BaseModel):
    credential: str
    id: CredentialId


class GcpCredentialUpdateInput(BaseModel):
    credential: str
    id: CredentialId


class GcpPubSubInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    project: str
    subscription_id: str = Field(alias="subscriptionId")


class GcpPubSubLiteInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    location: str
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    project: str
    subscription_id: str = Field(alias="subscriptionId")


class GcpPubSubLiteSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    location: str
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: str
    project: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    subscription_id: str = Field(alias="subscriptionId")


class GcpPubSubLiteSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )


class GcpPubSubSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: str
    project: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    subscription_id: str = Field(alias="subscriptionId")


class GcpPubSubSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )


class GcpStorageInferSchemaInput(BaseModel):
    bucket: str
    credential_id: CredentialId = Field(alias="credentialId")
    csv: Optional["CsvParserInput"] = None
    file_format: Optional[FileFormat] = Field(alias="fileFormat", default=None)
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    folder: str
    project: str


class GcpStorageSourceCreateInput(BaseModel):
    bucket: str
    credential_id: CredentialId = Field(alias="credentialId")
    csv: Optional["CsvParserInput"] = None
    file_format: Optional[FileFormat] = Field(alias="fileFormat", default=None)
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    folder: str
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    name: str
    project: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None


class GcpStorageSourceUpdateInput(BaseModel):
    csv: Optional["CsvParserInput"] = None
    file_pattern: Optional[str] = Field(alias="filePattern", default=None)
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    schedule: Optional[CronExpression] = None


class GlobalWindowCreateInput(BaseModel):
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_id: SourceId = Field(alias="sourceId")


class IdentityDeleteInput(BaseModel):
    id: str


class IdentityProviderDeleteInput(BaseModel):
    id: str


class IncidentsInput(BaseModel):
    time_range: "TimeRangeInput" = Field(alias="timeRange")


class KafkaInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    topic: str


class KafkaSaslSslPlainCredentialCreateInput(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    name: str
    password: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    username: str


class KafkaSaslSslPlainCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class KafkaSaslSslPlainCredentialUpdateInput(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    id: CredentialId
    password: str
    username: str


class KafkaSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    topic: str


class KafkaSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    message_format: Optional["StreamingSourceMessageFormatConfigInput"] = Field(
        alias="messageFormat", default=None
    )


class KafkaSslCredentialCreateInput(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")
    client_certificate: str = Field(alias="clientCertificate")
    client_private_key: str = Field(alias="clientPrivateKey")
    client_private_key_password: str = Field(alias="clientPrivateKeyPassword")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class KafkaSslCredentialSecretChangedInput(BaseModel):
    ca_certificate: str = Field(alias="caCertificate")
    client_certificate: str = Field(alias="clientCertificate")
    client_private_key: str = Field(alias="clientPrivateKey")
    client_private_key_password: str = Field(alias="clientPrivateKeyPassword")
    id: CredentialId


class KafkaSslCredentialUpdateInput(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")
    client_certificate: str = Field(alias="clientCertificate")
    client_private_key: str = Field(alias="clientPrivateKey")
    client_private_key_password: str = Field(alias="clientPrivateKeyPassword")
    id: CredentialId


class LocalIdentityProviderUpdateInput(BaseModel):
    disabled: bool
    id: str
    name: str


class NotificationRuleCreateInput(BaseModel):
    channel_id: Any = Field(alias="channelId")
    name: str
    notification_typenames: List[NotificationTypename] = Field(
        alias="notificationTypenames"
    )
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    sources: List[SourceId]


class NotificationRuleDeleteInput(BaseModel):
    id: Any


class NotificationRuleUpdateInput(BaseModel):
    channel_id: Optional[Any] = Field(alias="channelId", default=None)
    id: Any
    name: Optional[str] = None
    notification_typenames: List[NotificationTypename] = Field(
        alias="notificationTypenames"
    )
    sources: List[SourceId]


class NumericAnomalyValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: NumericAnomalyMetric
    minimum_absolute_difference: float = Field(alias="minimumAbsoluteDifference")
    minimum_reference_datapoints: Optional[float] = Field(
        alias="minimumReferenceDatapoints", default=None
    )
    minimum_relative_difference_percent: float = Field(
        alias="minimumRelativeDifferencePercent"
    )
    name: Optional[str] = None
    reference_source_config: "ReferenceSourceConfigCreateInput" = Field(
        alias="referenceSourceConfig"
    )
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    sensitivity: float
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: JsonPointer = Field(alias="sourceField")


class NumericAnomalyValidatorUpdateInput(BaseModel):
    id: ValidatorId
    reference_source_config: "ReferenceSourceConfigUpdateInput" = Field(
        alias="referenceSourceConfig"
    )
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class NumericDistributionValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: NumericDistributionMetric
    name: Optional[str] = None
    reference_source_config: "ReferenceSourceConfigCreateInput" = Field(
        alias="referenceSourceConfig"
    )
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: JsonPointer = Field(alias="sourceField")


class NumericDistributionValidatorUpdateInput(BaseModel):
    id: ValidatorId
    reference_source_config: "ReferenceSourceConfigUpdateInput" = Field(
        alias="referenceSourceConfig"
    )
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class NumericValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: NumericMetric
    name: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: JsonPointer = Field(alias="sourceField")


class NumericValidatorUpdateInput(BaseModel):
    id: ValidatorId
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class PostgreSqlCredentialCreateInput(BaseModel):
    default_database: str = Field(alias="defaultDatabase")
    host: str
    name: str
    password: str
    port: int
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    user: str


class PostgreSqlCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class PostgreSqlCredentialUpdateInput(BaseModel):
    default_database: str = Field(alias="defaultDatabase")
    host: str
    id: CredentialId
    password: str
    port: int
    user: str


class PostgreSqlInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    database: Optional[str] = None
    db_schema: str = Field(alias="schema")
    table: str


class PostgreSqlSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: Optional[str] = None
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    schedule: Optional[CronExpression] = None
    db_schema: str = Field(alias="schema")
    table: str


class PostgreSqlSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression] = None


class ReferenceSourceConfigCreateInput(BaseModel):
    filter: Optional[
        Annotated[
            JsonFilterExpression, PlainSerializer(serialize_json_filter_expression)
        ]
    ] = None
    history: int
    offset: int
    source_id: SourceId = Field(alias="sourceId")
    window_id: WindowId = Field(alias="windowId")


class ReferenceSourceConfigUpdateInput(BaseModel):
    filter: Optional[
        Annotated[
            JsonFilterExpression, PlainSerializer(serialize_json_filter_expression)
        ]
    ] = None
    history: int
    offset: int


class RelativeTimeValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: RelativeTimeMetric
    name: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")


class RelativeTimeValidatorUpdateInput(BaseModel):
    id: ValidatorId
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class RelativeVolumeValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: RelativeVolumeMetric
    name: Optional[str] = None
    reference_source_config: "ReferenceSourceConfigCreateInput" = Field(
        alias="referenceSourceConfig"
    )
    reference_source_field: Optional[JsonPointer] = Field(
        alias="referenceSourceField", default=None
    )
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: Optional[JsonPointer] = Field(alias="sourceField", default=None)


class RelativeVolumeValidatorUpdateInput(BaseModel):
    id: ValidatorId
    reference_source_config: "ReferenceSourceConfigUpdateInput" = Field(
        alias="referenceSourceConfig"
    )
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class ResourceFilter(BaseModel):
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class ResourceNamespaceUpdateInput(BaseModel):
    new_resource_namespace: str = Field(alias="newResourceNamespace")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class SamlIdentityProviderCreateInput(BaseModel):
    cert: str
    disabled: bool
    entity_id: str = Field(alias="entityId")
    entry_point: str = Field(alias="entryPoint")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class SamlIdentityProviderUpdateInput(BaseModel):
    cert: str
    disabled: bool
    entity_id: str = Field(alias="entityId")
    entry_point: str = Field(alias="entryPoint")
    id: str
    name: str


class SegmentIncidentsInput(BaseModel):
    segment_id: Any = Field(alias="segmentId")
    time_range: "TimeRangeInput" = Field(alias="timeRange")


class SegmentationCreateInput(BaseModel):
    fields: List[str]
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_id: SourceId = Field(alias="sourceId")


class SlackChannelCreateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    timezone: Optional[str] = None
    webhook_url: str = Field(alias="webhookUrl")


class SlackChannelUpdateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    id: Any
    name: Optional[str] = None
    timezone: Optional[str] = None
    webhook_url: str = Field(alias="webhookUrl")


class SnowflakeCredentialCreateInput(BaseModel):
    account: str
    name: str
    password: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    role: Optional[str] = None
    user: str
    warehouse: Optional[str] = None


class SnowflakeCredentialSecretChangedInput(BaseModel):
    id: CredentialId
    password: str


class SnowflakeCredentialUpdateInput(BaseModel):
    account: str
    id: CredentialId
    password: str
    role: Optional[str] = None
    user: str
    warehouse: Optional[str] = None


class SnowflakeInferSchemaInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    database: str
    role: Optional[str] = None
    db_schema: str = Field(alias="schema")
    table: str
    warehouse: Optional[str] = None


class SnowflakeSourceCreateInput(BaseModel):
    credential_id: CredentialId = Field(alias="credentialId")
    cursor_field: Optional[str] = Field(alias="cursorField", default=None)
    database: str
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    role: Optional[str] = None
    schedule: Optional[CronExpression] = None
    db_schema: str = Field(alias="schema")
    table: str
    warehouse: Optional[str] = None


class SnowflakeSourceUpdateInput(BaseModel):
    id: SourceId
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression] = None


class SourceConfigCreateInput(BaseModel):
    filter: Optional[
        Annotated[
            JsonFilterExpression, PlainSerializer(serialize_json_filter_expression)
        ]
    ] = None
    segmentation_id: SegmentationId = Field(alias="segmentationId")
    source_id: SourceId = Field(alias="sourceId")
    window_id: WindowId = Field(alias="windowId")


class SourceConfigUpdateInput(BaseModel):
    filter: Optional[
        Annotated[
            JsonFilterExpression, PlainSerializer(serialize_json_filter_expression)
        ]
    ] = None


class SourceIncidentsInput(BaseModel):
    source_id: SourceId = Field(alias="sourceId")
    time_range: "TimeRangeInput" = Field(alias="timeRange")


class SqlValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    name: Optional[str] = None
    query: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")


class StreamingSourceMessageFormatConfigInput(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema", default=None)


class TimeRangeInput(BaseModel):
    end: Annotated[datetime, PlainSerializer(serialize_rfc3339_datetime)]
    start: Annotated[datetime, PlainSerializer(serialize_rfc3339_datetime)]


class TumblingWindowCreateInput(BaseModel):
    data_time_field: JsonPointer = Field(alias="dataTimeField")
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_id: SourceId = Field(alias="sourceId")
    time_unit: WindowTimeUnit = Field(alias="timeUnit")
    window_size: int = Field(alias="windowSize")


class TumblingWindowUpdateInput(BaseModel):
    id: WindowId
    time_unit: WindowTimeUnit = Field(alias="timeUnit")
    window_size: int = Field(alias="windowSize")


class UserCreateInput(BaseModel):
    display_name: str = Field(alias="displayName")
    email: str
    full_name: Optional[str] = Field(alias="fullName", default=None)
    password: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    role: Role
    status: UserStatus
    username: Optional[str] = None


class UserDeleteInput(BaseModel):
    id: str


class UserUpdateInput(BaseModel):
    display_name: str = Field(alias="displayName")
    email: Optional[str] = None
    full_name: Optional[str] = Field(alias="fullName", default=None)
    id: str
    password: Optional[str] = None
    role: Role
    status: UserStatus
    username: Optional[str] = None


class ValidatorIncidentsInput(BaseModel):
    time_range: "TimeRangeInput" = Field(alias="timeRange")
    validator_id: ValidatorId = Field(alias="validatorId")


class ValidatorMetricDebugInfoInput(BaseModel):
    incident_id: Any = Field(alias="incidentId")


class ValidatorRecommendationApplyInput(BaseModel):
    ids: List[Any]
    initialize_with_backfill: Optional[bool] = Field(
        alias="initializeWithBackfill", default=None
    )
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)


class ValidatorRecommendationDismissInput(BaseModel):
    ids: List[Any]


class ValidatorSegmentIncidentsInput(BaseModel):
    segment_id: Any = Field(alias="segmentId")
    time_range: "TimeRangeInput" = Field(alias="timeRange")
    validator_id: ValidatorId = Field(alias="validatorId")


class ValidatorSegmentMetricsInput(BaseModel):
    segment_id: Any = Field(alias="segmentId")
    time_range: "TimeRangeInput" = Field(alias="timeRange")
    validator_id: ValidatorId = Field(alias="validatorId")


class ValidatorWithDynamicThresholdUpdateInput(BaseModel):
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType", default=None
    )
    sensitivity: float
    validator_id: ValidatorId = Field(alias="validatorId")


class ValidatorWithFixedThresholdUpdateInput(BaseModel):
    operator: ComparisonOperator
    validator_id: ValidatorId = Field(alias="validatorId")
    value: float


class VolumeValidatorCreateInput(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    metric: VolumeMetric
    name: Optional[str] = None
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    source_config: "SourceConfigCreateInput" = Field(alias="sourceConfig")
    source_field: Optional[JsonPointer] = Field(alias="sourceField", default=None)
    source_fields: List[JsonPointer] = Field(alias="sourceFields")


class VolumeValidatorUpdateInput(BaseModel):
    id: ValidatorId
    source_config: "SourceConfigUpdateInput" = Field(alias="sourceConfig")


class WebhookChannelCreateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader", default=None)
    name: str
    resource_name: Optional[str] = Field(alias="resourceName", default=None)
    resource_namespace: Optional[str] = Field(alias="resourceNamespace", default=None)
    webhook_url: str = Field(alias="webhookUrl")


class WebhookChannelUpdateInput(BaseModel):
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader", default=None)
    id: Any
    name: Optional[str] = None
    webhook_url: str = Field(alias="webhookUrl")


AwsAthenaCredentialCreateInput.model_rebuild()
AwsAthenaCredentialSecretChangedInput.model_rebuild()
AwsAthenaCredentialUpdateInput.model_rebuild()
AwsAthenaInferSchemaInput.model_rebuild()
AwsAthenaSourceCreateInput.model_rebuild()
AwsAthenaSourceUpdateInput.model_rebuild()
AwsCredentialCreateInput.model_rebuild()
AwsCredentialSecretChangedInput.model_rebuild()
AwsCredentialUpdateInput.model_rebuild()
AwsKinesisInferSchemaInput.model_rebuild()
AwsKinesisSourceCreateInput.model_rebuild()
AwsKinesisSourceUpdateInput.model_rebuild()
AwsRedshiftCredentialCreateInput.model_rebuild()
AwsRedshiftCredentialSecretChangedInput.model_rebuild()
AwsRedshiftCredentialUpdateInput.model_rebuild()
AwsRedshiftInferSchemaInput.model_rebuild()
AwsRedshiftSourceCreateInput.model_rebuild()
AwsRedshiftSourceUpdateInput.model_rebuild()
AwsS3InferSchemaInput.model_rebuild()
AwsS3SourceCreateInput.model_rebuild()
AwsS3SourceUpdateInput.model_rebuild()
CategoricalDistributionValidatorCreateInput.model_rebuild()
CategoricalDistributionValidatorUpdateInput.model_rebuild()
ChannelDeleteInput.model_rebuild()
CsvParserInput.model_rebuild()
DatabricksCredentialCreateInput.model_rebuild()
DatabricksCredentialSecretChangedInput.model_rebuild()
DatabricksCredentialUpdateInput.model_rebuild()
DatabricksInferSchemaInput.model_rebuild()
DatabricksListCatalogsInput.model_rebuild()
DatabricksListSchemasInput.model_rebuild()
DatabricksListTablesInput.model_rebuild()
DatabricksListWarehousesInput.model_rebuild()
DatabricksSourceCreateInput.model_rebuild()
DatabricksSourceUpdateInput.model_rebuild()
DbtArtifactUploadInput.model_rebuild()
DemoCredentialCreateInput.model_rebuild()
DemoSourceCreateInput.model_rebuild()
DynamicThresholdCreateInput.model_rebuild()
FileWindowCreateInput.model_rebuild()
FixedBatchWindowCreateInput.model_rebuild()
FixedBatchWindowUpdateInput.model_rebuild()
FixedThresholdCreateInput.model_rebuild()
FreshnessValidatorCreateInput.model_rebuild()
FreshnessValidatorUpdateInput.model_rebuild()
GcpBigQueryInferSchemaInput.model_rebuild()
GcpBigQuerySourceCreateInput.model_rebuild()
GcpBigQuerySourceUpdateInput.model_rebuild()
GcpCredentialCreateInput.model_rebuild()
GcpCredentialSecretChangedInput.model_rebuild()
GcpCredentialUpdateInput.model_rebuild()
GcpPubSubInferSchemaInput.model_rebuild()
GcpPubSubLiteInferSchemaInput.model_rebuild()
GcpPubSubLiteSourceCreateInput.model_rebuild()
GcpPubSubLiteSourceUpdateInput.model_rebuild()
GcpPubSubSourceCreateInput.model_rebuild()
GcpPubSubSourceUpdateInput.model_rebuild()
GcpStorageInferSchemaInput.model_rebuild()
GcpStorageSourceCreateInput.model_rebuild()
GcpStorageSourceUpdateInput.model_rebuild()
GlobalWindowCreateInput.model_rebuild()
IdentityDeleteInput.model_rebuild()
IdentityProviderDeleteInput.model_rebuild()
IncidentsInput.model_rebuild()
KafkaInferSchemaInput.model_rebuild()
KafkaSaslSslPlainCredentialCreateInput.model_rebuild()
KafkaSaslSslPlainCredentialSecretChangedInput.model_rebuild()
KafkaSaslSslPlainCredentialUpdateInput.model_rebuild()
KafkaSourceCreateInput.model_rebuild()
KafkaSourceUpdateInput.model_rebuild()
KafkaSslCredentialCreateInput.model_rebuild()
KafkaSslCredentialSecretChangedInput.model_rebuild()
KafkaSslCredentialUpdateInput.model_rebuild()
LocalIdentityProviderUpdateInput.model_rebuild()
NotificationRuleCreateInput.model_rebuild()
NotificationRuleDeleteInput.model_rebuild()
NotificationRuleUpdateInput.model_rebuild()
NumericAnomalyValidatorCreateInput.model_rebuild()
NumericAnomalyValidatorUpdateInput.model_rebuild()
NumericDistributionValidatorCreateInput.model_rebuild()
NumericDistributionValidatorUpdateInput.model_rebuild()
NumericValidatorCreateInput.model_rebuild()
NumericValidatorUpdateInput.model_rebuild()
PostgreSqlCredentialCreateInput.model_rebuild()
PostgreSqlCredentialSecretChangedInput.model_rebuild()
PostgreSqlCredentialUpdateInput.model_rebuild()
PostgreSqlInferSchemaInput.model_rebuild()
PostgreSqlSourceCreateInput.model_rebuild()
PostgreSqlSourceUpdateInput.model_rebuild()
ReferenceSourceConfigCreateInput.model_rebuild()
ReferenceSourceConfigUpdateInput.model_rebuild()
RelativeTimeValidatorCreateInput.model_rebuild()
RelativeTimeValidatorUpdateInput.model_rebuild()
RelativeVolumeValidatorCreateInput.model_rebuild()
RelativeVolumeValidatorUpdateInput.model_rebuild()
ResourceFilter.model_rebuild()
ResourceNamespaceUpdateInput.model_rebuild()
SamlIdentityProviderCreateInput.model_rebuild()
SamlIdentityProviderUpdateInput.model_rebuild()
SegmentIncidentsInput.model_rebuild()
SegmentationCreateInput.model_rebuild()
SlackChannelCreateInput.model_rebuild()
SlackChannelUpdateInput.model_rebuild()
SnowflakeCredentialCreateInput.model_rebuild()
SnowflakeCredentialSecretChangedInput.model_rebuild()
SnowflakeCredentialUpdateInput.model_rebuild()
SnowflakeInferSchemaInput.model_rebuild()
SnowflakeSourceCreateInput.model_rebuild()
SnowflakeSourceUpdateInput.model_rebuild()
SourceConfigCreateInput.model_rebuild()
SourceConfigUpdateInput.model_rebuild()
SourceIncidentsInput.model_rebuild()
SqlValidatorCreateInput.model_rebuild()
StreamingSourceMessageFormatConfigInput.model_rebuild()
TimeRangeInput.model_rebuild()
TumblingWindowCreateInput.model_rebuild()
TumblingWindowUpdateInput.model_rebuild()
UserCreateInput.model_rebuild()
UserDeleteInput.model_rebuild()
UserUpdateInput.model_rebuild()
ValidatorIncidentsInput.model_rebuild()
ValidatorMetricDebugInfoInput.model_rebuild()
ValidatorRecommendationApplyInput.model_rebuild()
ValidatorRecommendationDismissInput.model_rebuild()
ValidatorSegmentIncidentsInput.model_rebuild()
ValidatorSegmentMetricsInput.model_rebuild()
ValidatorWithDynamicThresholdUpdateInput.model_rebuild()
ValidatorWithFixedThresholdUpdateInput.model_rebuild()
VolumeValidatorCreateInput.model_rebuild()
VolumeValidatorUpdateInput.model_rebuild()
WebhookChannelCreateInput.model_rebuild()
WebhookChannelUpdateInput.model_rebuild()
