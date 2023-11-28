from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import CredentialId

from .base_model import BaseModel


class GetCredentialByResourceName(BaseModel):
    credential_by_resource_name: Optional[
        Annotated[
            Union[
                "GetCredentialByResourceNameCredentialByResourceNameCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential",
                "GetCredentialByResourceNameCredentialByResourceNameDatabricksCredential",
                "GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredential",
                "GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredential",
                "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential",
                "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="credentialByResourceName")


class GetCredentialByResourceNameCredentialByResourceNameCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential", "GcpCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential(BaseModel):
    typename__: Literal["AwsAthenaCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig(
    BaseModel
):
    access_key: str = Field(alias="accessKey")
    region: str
    query_result_location: str = Field(alias="queryResultLocation")


class GetCredentialByResourceNameCredentialByResourceNameAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential(
    BaseModel
):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameDatabricksCredential(
    BaseModel
):
    typename__: Literal["DatabricksCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameDatabricksCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameDatabricksCredentialConfig(
    BaseModel
):
    host: str
    port: int


class GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredential(
    BaseModel
):
    typename__: Literal["KafkaSaslSslPlainCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredentialConfig(
    BaseModel
):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    username: str


class GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredential(BaseModel):
    typename__: Literal["KafkaSslCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredentialConfig(
    BaseModel
):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential(
    BaseModel
):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig(
    BaseModel
):
    account: str
    user: str
    role: Optional[str]
    warehouse: Optional[str]


GetCredentialByResourceName.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsAthenaCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDatabricksCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameDatabricksCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameKafkaSaslSslPlainCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameKafkaSslCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential.model_rebuild()
GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig.model_rebuild()
