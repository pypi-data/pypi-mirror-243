from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import CredentialId

from .base_model import BaseModel


class ListCredentials(BaseModel):
    credentials_list: List[
        Annotated[
            Union[
                "ListCredentialsCredentialsListCredential",
                "ListCredentialsCredentialsListAwsAthenaCredential",
                "ListCredentialsCredentialsListAwsCredential",
                "ListCredentialsCredentialsListAwsRedshiftCredential",
                "ListCredentialsCredentialsListDatabricksCredential",
                "ListCredentialsCredentialsListKafkaSaslSslPlainCredential",
                "ListCredentialsCredentialsListKafkaSslCredential",
                "ListCredentialsCredentialsListPostgreSqlCredential",
                "ListCredentialsCredentialsListSnowflakeCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="credentialsList")


class ListCredentialsCredentialsListCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential", "GcpCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListCredentialsCredentialsListAwsAthenaCredential(BaseModel):
    typename__: Literal["AwsAthenaCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAwsAthenaCredentialConfig"


class ListCredentialsCredentialsListAwsAthenaCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")
    region: str
    query_result_location: str = Field(alias="queryResultLocation")


class ListCredentialsCredentialsListAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAwsCredentialConfig"


class ListCredentialsCredentialsListAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class ListCredentialsCredentialsListAwsRedshiftCredential(BaseModel):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAwsRedshiftCredentialConfig"


class ListCredentialsCredentialsListAwsRedshiftCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class ListCredentialsCredentialsListDatabricksCredential(BaseModel):
    typename__: Literal["DatabricksCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListDatabricksCredentialConfig"


class ListCredentialsCredentialsListDatabricksCredentialConfig(BaseModel):
    host: str
    port: int


class ListCredentialsCredentialsListKafkaSaslSslPlainCredential(BaseModel):
    typename__: Literal["KafkaSaslSslPlainCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListKafkaSaslSslPlainCredentialConfig"


class ListCredentialsCredentialsListKafkaSaslSslPlainCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    username: str


class ListCredentialsCredentialsListKafkaSslCredential(BaseModel):
    typename__: Literal["KafkaSslCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListKafkaSslCredentialConfig"


class ListCredentialsCredentialsListKafkaSslCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")


class ListCredentialsCredentialsListPostgreSqlCredential(BaseModel):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListPostgreSqlCredentialConfig"


class ListCredentialsCredentialsListPostgreSqlCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class ListCredentialsCredentialsListSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListSnowflakeCredentialConfig"


class ListCredentialsCredentialsListSnowflakeCredentialConfig(BaseModel):
    account: str
    user: str
    role: Optional[str]
    warehouse: Optional[str]


ListCredentials.model_rebuild()
ListCredentialsCredentialsListCredential.model_rebuild()
ListCredentialsCredentialsListAwsAthenaCredential.model_rebuild()
ListCredentialsCredentialsListAwsAthenaCredentialConfig.model_rebuild()
ListCredentialsCredentialsListAwsCredential.model_rebuild()
ListCredentialsCredentialsListAwsCredentialConfig.model_rebuild()
ListCredentialsCredentialsListAwsRedshiftCredential.model_rebuild()
ListCredentialsCredentialsListAwsRedshiftCredentialConfig.model_rebuild()
ListCredentialsCredentialsListDatabricksCredential.model_rebuild()
ListCredentialsCredentialsListDatabricksCredentialConfig.model_rebuild()
ListCredentialsCredentialsListKafkaSaslSslPlainCredential.model_rebuild()
ListCredentialsCredentialsListKafkaSaslSslPlainCredentialConfig.model_rebuild()
ListCredentialsCredentialsListKafkaSslCredential.model_rebuild()
ListCredentialsCredentialsListKafkaSslCredentialConfig.model_rebuild()
ListCredentialsCredentialsListPostgreSqlCredential.model_rebuild()
ListCredentialsCredentialsListPostgreSqlCredentialConfig.model_rebuild()
ListCredentialsCredentialsListSnowflakeCredential.model_rebuild()
ListCredentialsCredentialsListSnowflakeCredentialConfig.model_rebuild()
