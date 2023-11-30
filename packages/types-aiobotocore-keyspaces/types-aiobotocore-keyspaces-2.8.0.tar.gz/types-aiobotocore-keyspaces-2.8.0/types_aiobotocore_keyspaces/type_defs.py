"""
Type annotations for keyspaces service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/type_defs/)

Usage::

    ```python
    from types_aiobotocore_keyspaces.type_defs import CapacitySpecificationSummaryTypeDef

    data: CapacitySpecificationSummaryTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    EncryptionTypeType,
    PointInTimeRecoveryStatusType,
    SortOrderType,
    TableStatusType,
    ThroughputModeType,
    rsType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CapacitySpecificationSummaryTypeDef",
    "CapacitySpecificationTypeDef",
    "ClientSideTimestampsTypeDef",
    "ClusteringKeyTypeDef",
    "ColumnDefinitionTypeDef",
    "CommentTypeDef",
    "ReplicationSpecificationTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "EncryptionSpecificationTypeDef",
    "PointInTimeRecoveryTypeDef",
    "TimeToLiveTypeDef",
    "DeleteKeyspaceRequestRequestTypeDef",
    "DeleteTableRequestRequestTypeDef",
    "GetKeyspaceRequestRequestTypeDef",
    "GetTableRequestRequestTypeDef",
    "PointInTimeRecoverySummaryTypeDef",
    "KeyspaceSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ListKeyspacesRequestRequestTypeDef",
    "ListTablesRequestRequestTypeDef",
    "TableSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PartitionKeyTypeDef",
    "TimestampTypeDef",
    "StaticColumnTypeDef",
    "CreateKeyspaceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "CreateKeyspaceResponseTypeDef",
    "CreateTableResponseTypeDef",
    "GetKeyspaceResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RestoreTableResponseTypeDef",
    "UpdateTableResponseTypeDef",
    "UpdateTableRequestRequestTypeDef",
    "ListKeyspacesResponseTypeDef",
    "ListKeyspacesRequestListKeyspacesPaginateTypeDef",
    "ListTablesRequestListTablesPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTablesResponseTypeDef",
    "RestoreTableRequestRequestTypeDef",
    "SchemaDefinitionTypeDef",
    "CreateTableRequestRequestTypeDef",
    "GetTableResponseTypeDef",
)

CapacitySpecificationSummaryTypeDef = TypedDict(
    "CapacitySpecificationSummaryTypeDef",
    {
        "throughputMode": ThroughputModeType,
        "readCapacityUnits": NotRequired[int],
        "writeCapacityUnits": NotRequired[int],
        "lastUpdateToPayPerRequestTimestamp": NotRequired[datetime],
    },
)
CapacitySpecificationTypeDef = TypedDict(
    "CapacitySpecificationTypeDef",
    {
        "throughputMode": ThroughputModeType,
        "readCapacityUnits": NotRequired[int],
        "writeCapacityUnits": NotRequired[int],
    },
)
ClientSideTimestampsTypeDef = TypedDict(
    "ClientSideTimestampsTypeDef",
    {
        "status": Literal["ENABLED"],
    },
)
ClusteringKeyTypeDef = TypedDict(
    "ClusteringKeyTypeDef",
    {
        "name": str,
        "orderBy": SortOrderType,
    },
)
ColumnDefinitionTypeDef = TypedDict(
    "ColumnDefinitionTypeDef",
    {
        "name": str,
        "type": str,
    },
)
CommentTypeDef = TypedDict(
    "CommentTypeDef",
    {
        "message": str,
    },
)
ReplicationSpecificationTypeDef = TypedDict(
    "ReplicationSpecificationTypeDef",
    {
        "replicationStrategy": rsType,
        "regionList": NotRequired[Sequence[str]],
    },
)
TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)
EncryptionSpecificationTypeDef = TypedDict(
    "EncryptionSpecificationTypeDef",
    {
        "type": EncryptionTypeType,
        "kmsKeyIdentifier": NotRequired[str],
    },
)
PointInTimeRecoveryTypeDef = TypedDict(
    "PointInTimeRecoveryTypeDef",
    {
        "status": PointInTimeRecoveryStatusType,
    },
)
TimeToLiveTypeDef = TypedDict(
    "TimeToLiveTypeDef",
    {
        "status": Literal["ENABLED"],
    },
)
DeleteKeyspaceRequestRequestTypeDef = TypedDict(
    "DeleteKeyspaceRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)
DeleteTableRequestRequestTypeDef = TypedDict(
    "DeleteTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
    },
)
GetKeyspaceRequestRequestTypeDef = TypedDict(
    "GetKeyspaceRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)
GetTableRequestRequestTypeDef = TypedDict(
    "GetTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
    },
)
PointInTimeRecoverySummaryTypeDef = TypedDict(
    "PointInTimeRecoverySummaryTypeDef",
    {
        "status": PointInTimeRecoveryStatusType,
        "earliestRestorableTimestamp": NotRequired[datetime],
    },
)
KeyspaceSummaryTypeDef = TypedDict(
    "KeyspaceSummaryTypeDef",
    {
        "keyspaceName": str,
        "resourceArn": str,
        "replicationStrategy": rsType,
        "replicationRegions": NotRequired[List[str]],
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ListKeyspacesRequestRequestTypeDef = TypedDict(
    "ListKeyspacesRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListTablesRequestRequestTypeDef = TypedDict(
    "ListTablesRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
TableSummaryTypeDef = TypedDict(
    "TableSummaryTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "resourceArn": str,
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
PartitionKeyTypeDef = TypedDict(
    "PartitionKeyTypeDef",
    {
        "name": str,
    },
)
TimestampTypeDef = Union[datetime, str]
StaticColumnTypeDef = TypedDict(
    "StaticColumnTypeDef",
    {
        "name": str,
    },
)
CreateKeyspaceRequestRequestTypeDef = TypedDict(
    "CreateKeyspaceRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tags": NotRequired[Sequence[TagTypeDef]],
        "replicationSpecification": NotRequired[ReplicationSpecificationTypeDef],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)
CreateKeyspaceResponseTypeDef = TypedDict(
    "CreateKeyspaceResponseTypeDef",
    {
        "resourceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateTableResponseTypeDef = TypedDict(
    "CreateTableResponseTypeDef",
    {
        "resourceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetKeyspaceResponseTypeDef = TypedDict(
    "GetKeyspaceResponseTypeDef",
    {
        "keyspaceName": str,
        "resourceArn": str,
        "replicationStrategy": rsType,
        "replicationRegions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "nextToken": str,
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RestoreTableResponseTypeDef = TypedDict(
    "RestoreTableResponseTypeDef",
    {
        "restoredTableARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTableResponseTypeDef = TypedDict(
    "UpdateTableResponseTypeDef",
    {
        "resourceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTableRequestRequestTypeDef = TypedDict(
    "UpdateTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "addColumns": NotRequired[Sequence[ColumnDefinitionTypeDef]],
        "capacitySpecification": NotRequired[CapacitySpecificationTypeDef],
        "encryptionSpecification": NotRequired[EncryptionSpecificationTypeDef],
        "pointInTimeRecovery": NotRequired[PointInTimeRecoveryTypeDef],
        "ttl": NotRequired[TimeToLiveTypeDef],
        "defaultTimeToLive": NotRequired[int],
        "clientSideTimestamps": NotRequired[ClientSideTimestampsTypeDef],
    },
)
ListKeyspacesResponseTypeDef = TypedDict(
    "ListKeyspacesResponseTypeDef",
    {
        "nextToken": str,
        "keyspaces": List[KeyspaceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListKeyspacesRequestListKeyspacesPaginateTypeDef = TypedDict(
    "ListKeyspacesRequestListKeyspacesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTablesRequestListTablesPaginateTypeDef = TypedDict(
    "ListTablesRequestListTablesPaginateTypeDef",
    {
        "keyspaceName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "resourceArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTablesResponseTypeDef = TypedDict(
    "ListTablesResponseTypeDef",
    {
        "nextToken": str,
        "tables": List[TableSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RestoreTableRequestRequestTypeDef = TypedDict(
    "RestoreTableRequestRequestTypeDef",
    {
        "sourceKeyspaceName": str,
        "sourceTableName": str,
        "targetKeyspaceName": str,
        "targetTableName": str,
        "restoreTimestamp": NotRequired[TimestampTypeDef],
        "capacitySpecificationOverride": NotRequired[CapacitySpecificationTypeDef],
        "encryptionSpecificationOverride": NotRequired[EncryptionSpecificationTypeDef],
        "pointInTimeRecoveryOverride": NotRequired[PointInTimeRecoveryTypeDef],
        "tagsOverride": NotRequired[Sequence[TagTypeDef]],
    },
)
SchemaDefinitionTypeDef = TypedDict(
    "SchemaDefinitionTypeDef",
    {
        "allColumns": Sequence[ColumnDefinitionTypeDef],
        "partitionKeys": Sequence[PartitionKeyTypeDef],
        "clusteringKeys": NotRequired[Sequence[ClusteringKeyTypeDef]],
        "staticColumns": NotRequired[Sequence[StaticColumnTypeDef]],
    },
)
CreateTableRequestRequestTypeDef = TypedDict(
    "CreateTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "schemaDefinition": SchemaDefinitionTypeDef,
        "comment": NotRequired[CommentTypeDef],
        "capacitySpecification": NotRequired[CapacitySpecificationTypeDef],
        "encryptionSpecification": NotRequired[EncryptionSpecificationTypeDef],
        "pointInTimeRecovery": NotRequired[PointInTimeRecoveryTypeDef],
        "ttl": NotRequired[TimeToLiveTypeDef],
        "defaultTimeToLive": NotRequired[int],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "clientSideTimestamps": NotRequired[ClientSideTimestampsTypeDef],
    },
)
GetTableResponseTypeDef = TypedDict(
    "GetTableResponseTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "resourceArn": str,
        "creationTimestamp": datetime,
        "status": TableStatusType,
        "schemaDefinition": SchemaDefinitionTypeDef,
        "capacitySpecification": CapacitySpecificationSummaryTypeDef,
        "encryptionSpecification": EncryptionSpecificationTypeDef,
        "pointInTimeRecovery": PointInTimeRecoverySummaryTypeDef,
        "ttl": TimeToLiveTypeDef,
        "defaultTimeToLive": int,
        "comment": CommentTypeDef,
        "clientSideTimestamps": ClientSideTimestampsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
