"""
Type annotations for cleanrooms service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/type_defs/)

Usage::

    ```python
    from types_aiobotocore_cleanrooms.type_defs import AggregateColumnTypeDef

    data: AggregateColumnTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AggregateFunctionNameType,
    AnalysisRuleTypeType,
    CollaborationQueryLogStatusType,
    ConfiguredTableAnalysisRuleTypeType,
    FilterableMemberStatusType,
    JoinOperatorType,
    MemberAbilityType,
    MembershipQueryLogStatusType,
    MembershipStatusType,
    MemberStatusType,
    ParameterTypeType,
    ProtectedQueryStatusType,
    ResultFormatType,
    ScalarFunctionsType,
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
    "AggregateColumnTypeDef",
    "AggregationConstraintTypeDef",
    "AnalysisParameterTypeDef",
    "AnalysisRuleCustomTypeDef",
    "AnalysisRuleListTypeDef",
    "AnalysisSchemaTypeDef",
    "AnalysisSourceTypeDef",
    "AnalysisTemplateSummaryTypeDef",
    "BatchGetCollaborationAnalysisTemplateErrorTypeDef",
    "BatchGetCollaborationAnalysisTemplateInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BatchGetSchemaErrorTypeDef",
    "BatchGetSchemaInputRequestTypeDef",
    "CollaborationAnalysisTemplateSummaryTypeDef",
    "CollaborationSummaryTypeDef",
    "DataEncryptionMetadataTypeDef",
    "ColumnTypeDef",
    "ConfiguredTableAssociationSummaryTypeDef",
    "ConfiguredTableAssociationTypeDef",
    "ConfiguredTableSummaryTypeDef",
    "CreateConfiguredTableAssociationInputRequestTypeDef",
    "DeleteAnalysisTemplateInputRequestTypeDef",
    "DeleteCollaborationInputRequestTypeDef",
    "DeleteConfiguredTableAnalysisRuleInputRequestTypeDef",
    "DeleteConfiguredTableAssociationInputRequestTypeDef",
    "DeleteConfiguredTableInputRequestTypeDef",
    "DeleteMemberInputRequestTypeDef",
    "DeleteMembershipInputRequestTypeDef",
    "GetAnalysisTemplateInputRequestTypeDef",
    "GetCollaborationAnalysisTemplateInputRequestTypeDef",
    "GetCollaborationInputRequestTypeDef",
    "GetConfiguredTableAnalysisRuleInputRequestTypeDef",
    "GetConfiguredTableAssociationInputRequestTypeDef",
    "GetConfiguredTableInputRequestTypeDef",
    "GetMembershipInputRequestTypeDef",
    "GetProtectedQueryInputRequestTypeDef",
    "GetSchemaAnalysisRuleInputRequestTypeDef",
    "GetSchemaInputRequestTypeDef",
    "GlueTableReferenceTypeDef",
    "PaginatorConfigTypeDef",
    "ListAnalysisTemplatesInputRequestTypeDef",
    "ListCollaborationAnalysisTemplatesInputRequestTypeDef",
    "ListCollaborationsInputRequestTypeDef",
    "ListConfiguredTableAssociationsInputRequestTypeDef",
    "ListConfiguredTablesInputRequestTypeDef",
    "ListMembersInputRequestTypeDef",
    "ListMembershipsInputRequestTypeDef",
    "ListProtectedQueriesInputRequestTypeDef",
    "ProtectedQuerySummaryTypeDef",
    "ListSchemasInputRequestTypeDef",
    "SchemaSummaryTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "MembershipQueryComputePaymentConfigTypeDef",
    "ProtectedQueryS3OutputConfigurationTypeDef",
    "QueryComputePaymentConfigTypeDef",
    "ProtectedQueryErrorTypeDef",
    "ProtectedQueryS3OutputTypeDef",
    "ProtectedQuerySingleMemberOutputTypeDef",
    "ProtectedQuerySQLParametersTypeDef",
    "ProtectedQueryStatisticsTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateAnalysisTemplateInputRequestTypeDef",
    "UpdateCollaborationInputRequestTypeDef",
    "UpdateConfiguredTableAssociationInputRequestTypeDef",
    "UpdateConfiguredTableInputRequestTypeDef",
    "UpdateProtectedQueryInputRequestTypeDef",
    "AnalysisRuleAggregationTypeDef",
    "AnalysisTemplateTypeDef",
    "CollaborationAnalysisTemplateTypeDef",
    "CreateAnalysisTemplateInputRequestTypeDef",
    "ListAnalysisTemplatesOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListCollaborationAnalysisTemplatesOutputTypeDef",
    "ListCollaborationsOutputTypeDef",
    "CollaborationTypeDef",
    "SchemaTypeDef",
    "ListConfiguredTableAssociationsOutputTypeDef",
    "CreateConfiguredTableAssociationOutputTypeDef",
    "GetConfiguredTableAssociationOutputTypeDef",
    "UpdateConfiguredTableAssociationOutputTypeDef",
    "ListConfiguredTablesOutputTypeDef",
    "TableReferenceTypeDef",
    "ListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef",
    "ListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef",
    "ListCollaborationsInputListCollaborationsPaginateTypeDef",
    "ListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef",
    "ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef",
    "ListMembersInputListMembersPaginateTypeDef",
    "ListMembershipsInputListMembershipsPaginateTypeDef",
    "ListProtectedQueriesInputListProtectedQueriesPaginateTypeDef",
    "ListSchemasInputListSchemasPaginateTypeDef",
    "ListProtectedQueriesOutputTypeDef",
    "ListSchemasOutputTypeDef",
    "MembershipPaymentConfigurationTypeDef",
    "MembershipProtectedQueryOutputConfigurationTypeDef",
    "ProtectedQueryOutputConfigurationTypeDef",
    "PaymentConfigurationTypeDef",
    "ProtectedQueryOutputTypeDef",
    "AnalysisRulePolicyV1TypeDef",
    "ConfiguredTableAnalysisRulePolicyV1TypeDef",
    "CreateAnalysisTemplateOutputTypeDef",
    "GetAnalysisTemplateOutputTypeDef",
    "UpdateAnalysisTemplateOutputTypeDef",
    "BatchGetCollaborationAnalysisTemplateOutputTypeDef",
    "GetCollaborationAnalysisTemplateOutputTypeDef",
    "CreateCollaborationOutputTypeDef",
    "GetCollaborationOutputTypeDef",
    "UpdateCollaborationOutputTypeDef",
    "BatchGetSchemaOutputTypeDef",
    "GetSchemaOutputTypeDef",
    "ConfiguredTableTypeDef",
    "CreateConfiguredTableInputRequestTypeDef",
    "MembershipSummaryTypeDef",
    "MembershipProtectedQueryResultConfigurationTypeDef",
    "ProtectedQueryResultConfigurationTypeDef",
    "MemberSpecificationTypeDef",
    "MemberSummaryTypeDef",
    "ProtectedQueryResultTypeDef",
    "AnalysisRulePolicyTypeDef",
    "ConfiguredTableAnalysisRulePolicyTypeDef",
    "CreateConfiguredTableOutputTypeDef",
    "GetConfiguredTableOutputTypeDef",
    "UpdateConfiguredTableOutputTypeDef",
    "ListMembershipsOutputTypeDef",
    "CreateMembershipInputRequestTypeDef",
    "MembershipTypeDef",
    "UpdateMembershipInputRequestTypeDef",
    "StartProtectedQueryInputRequestTypeDef",
    "CreateCollaborationInputRequestTypeDef",
    "ListMembersOutputTypeDef",
    "ProtectedQueryTypeDef",
    "AnalysisRuleTypeDef",
    "ConfiguredTableAnalysisRuleTypeDef",
    "CreateConfiguredTableAnalysisRuleInputRequestTypeDef",
    "UpdateConfiguredTableAnalysisRuleInputRequestTypeDef",
    "CreateMembershipOutputTypeDef",
    "GetMembershipOutputTypeDef",
    "UpdateMembershipOutputTypeDef",
    "GetProtectedQueryOutputTypeDef",
    "StartProtectedQueryOutputTypeDef",
    "UpdateProtectedQueryOutputTypeDef",
    "GetSchemaAnalysisRuleOutputTypeDef",
    "CreateConfiguredTableAnalysisRuleOutputTypeDef",
    "GetConfiguredTableAnalysisRuleOutputTypeDef",
    "UpdateConfiguredTableAnalysisRuleOutputTypeDef",
)

AggregateColumnTypeDef = TypedDict(
    "AggregateColumnTypeDef",
    {
        "columnNames": Sequence[str],
        "function": AggregateFunctionNameType,
    },
)
AggregationConstraintTypeDef = TypedDict(
    "AggregationConstraintTypeDef",
    {
        "columnName": str,
        "minimum": int,
        "type": Literal["COUNT_DISTINCT"],
    },
)
AnalysisParameterTypeDef = TypedDict(
    "AnalysisParameterTypeDef",
    {
        "name": str,
        "type": ParameterTypeType,
        "defaultValue": NotRequired[str],
    },
)
AnalysisRuleCustomTypeDef = TypedDict(
    "AnalysisRuleCustomTypeDef",
    {
        "allowedAnalyses": Sequence[str],
        "allowedAnalysisProviders": NotRequired[Sequence[str]],
    },
)
AnalysisRuleListTypeDef = TypedDict(
    "AnalysisRuleListTypeDef",
    {
        "joinColumns": Sequence[str],
        "listColumns": Sequence[str],
        "allowedJoinOperators": NotRequired[Sequence[JoinOperatorType]],
    },
)
AnalysisSchemaTypeDef = TypedDict(
    "AnalysisSchemaTypeDef",
    {
        "referencedTables": NotRequired[List[str]],
    },
)
AnalysisSourceTypeDef = TypedDict(
    "AnalysisSourceTypeDef",
    {
        "text": NotRequired[str],
    },
)
AnalysisTemplateSummaryTypeDef = TypedDict(
    "AnalysisTemplateSummaryTypeDef",
    {
        "arn": str,
        "createTime": datetime,
        "id": str,
        "name": str,
        "updateTime": datetime,
        "membershipArn": str,
        "membershipId": str,
        "collaborationArn": str,
        "collaborationId": str,
        "description": NotRequired[str],
    },
)
BatchGetCollaborationAnalysisTemplateErrorTypeDef = TypedDict(
    "BatchGetCollaborationAnalysisTemplateErrorTypeDef",
    {
        "arn": str,
        "code": str,
        "message": str,
    },
)
BatchGetCollaborationAnalysisTemplateInputRequestTypeDef = TypedDict(
    "BatchGetCollaborationAnalysisTemplateInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "analysisTemplateArns": Sequence[str],
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
BatchGetSchemaErrorTypeDef = TypedDict(
    "BatchGetSchemaErrorTypeDef",
    {
        "name": str,
        "code": str,
        "message": str,
    },
)
BatchGetSchemaInputRequestTypeDef = TypedDict(
    "BatchGetSchemaInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "names": Sequence[str],
    },
)
CollaborationAnalysisTemplateSummaryTypeDef = TypedDict(
    "CollaborationAnalysisTemplateSummaryTypeDef",
    {
        "arn": str,
        "createTime": datetime,
        "id": str,
        "name": str,
        "updateTime": datetime,
        "collaborationArn": str,
        "collaborationId": str,
        "creatorAccountId": str,
        "description": NotRequired[str],
    },
)
CollaborationSummaryTypeDef = TypedDict(
    "CollaborationSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "creatorAccountId": str,
        "creatorDisplayName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "memberStatus": MemberStatusType,
        "membershipId": NotRequired[str],
        "membershipArn": NotRequired[str],
    },
)
DataEncryptionMetadataTypeDef = TypedDict(
    "DataEncryptionMetadataTypeDef",
    {
        "allowCleartext": bool,
        "allowDuplicates": bool,
        "allowJoinsOnColumnsWithDifferentNames": bool,
        "preserveNulls": bool,
    },
)
ColumnTypeDef = TypedDict(
    "ColumnTypeDef",
    {
        "name": str,
        "type": str,
    },
)
ConfiguredTableAssociationSummaryTypeDef = TypedDict(
    "ConfiguredTableAssociationSummaryTypeDef",
    {
        "configuredTableId": str,
        "membershipId": str,
        "membershipArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "id": str,
        "arn": str,
    },
)
ConfiguredTableAssociationTypeDef = TypedDict(
    "ConfiguredTableAssociationTypeDef",
    {
        "arn": str,
        "id": str,
        "configuredTableId": str,
        "configuredTableArn": str,
        "membershipId": str,
        "membershipArn": str,
        "roleArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "description": NotRequired[str],
    },
)
ConfiguredTableSummaryTypeDef = TypedDict(
    "ConfiguredTableSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "analysisRuleTypes": List[ConfiguredTableAnalysisRuleTypeType],
        "analysisMethod": Literal["DIRECT_QUERY"],
    },
)
CreateConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "CreateConfiguredTableAssociationInputRequestTypeDef",
    {
        "name": str,
        "membershipIdentifier": str,
        "configuredTableIdentifier": str,
        "roleArn": str,
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
DeleteAnalysisTemplateInputRequestTypeDef = TypedDict(
    "DeleteAnalysisTemplateInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "analysisTemplateIdentifier": str,
    },
)
DeleteCollaborationInputRequestTypeDef = TypedDict(
    "DeleteCollaborationInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
    },
)
DeleteConfiguredTableAnalysisRuleInputRequestTypeDef = TypedDict(
    "DeleteConfiguredTableAnalysisRuleInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
        "analysisRuleType": ConfiguredTableAnalysisRuleTypeType,
    },
)
DeleteConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "DeleteConfiguredTableAssociationInputRequestTypeDef",
    {
        "configuredTableAssociationIdentifier": str,
        "membershipIdentifier": str,
    },
)
DeleteConfiguredTableInputRequestTypeDef = TypedDict(
    "DeleteConfiguredTableInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
    },
)
DeleteMemberInputRequestTypeDef = TypedDict(
    "DeleteMemberInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "accountId": str,
    },
)
DeleteMembershipInputRequestTypeDef = TypedDict(
    "DeleteMembershipInputRequestTypeDef",
    {
        "membershipIdentifier": str,
    },
)
GetAnalysisTemplateInputRequestTypeDef = TypedDict(
    "GetAnalysisTemplateInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "analysisTemplateIdentifier": str,
    },
)
GetCollaborationAnalysisTemplateInputRequestTypeDef = TypedDict(
    "GetCollaborationAnalysisTemplateInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "analysisTemplateArn": str,
    },
)
GetCollaborationInputRequestTypeDef = TypedDict(
    "GetCollaborationInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
    },
)
GetConfiguredTableAnalysisRuleInputRequestTypeDef = TypedDict(
    "GetConfiguredTableAnalysisRuleInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
        "analysisRuleType": ConfiguredTableAnalysisRuleTypeType,
    },
)
GetConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "GetConfiguredTableAssociationInputRequestTypeDef",
    {
        "configuredTableAssociationIdentifier": str,
        "membershipIdentifier": str,
    },
)
GetConfiguredTableInputRequestTypeDef = TypedDict(
    "GetConfiguredTableInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
    },
)
GetMembershipInputRequestTypeDef = TypedDict(
    "GetMembershipInputRequestTypeDef",
    {
        "membershipIdentifier": str,
    },
)
GetProtectedQueryInputRequestTypeDef = TypedDict(
    "GetProtectedQueryInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "protectedQueryIdentifier": str,
    },
)
GetSchemaAnalysisRuleInputRequestTypeDef = TypedDict(
    "GetSchemaAnalysisRuleInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "name": str,
        "type": AnalysisRuleTypeType,
    },
)
GetSchemaInputRequestTypeDef = TypedDict(
    "GetSchemaInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "name": str,
    },
)
GlueTableReferenceTypeDef = TypedDict(
    "GlueTableReferenceTypeDef",
    {
        "tableName": str,
        "databaseName": str,
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
ListAnalysisTemplatesInputRequestTypeDef = TypedDict(
    "ListAnalysisTemplatesInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListCollaborationAnalysisTemplatesInputRequestTypeDef = TypedDict(
    "ListCollaborationAnalysisTemplatesInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListCollaborationsInputRequestTypeDef = TypedDict(
    "ListCollaborationsInputRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "memberStatus": NotRequired[FilterableMemberStatusType],
    },
)
ListConfiguredTableAssociationsInputRequestTypeDef = TypedDict(
    "ListConfiguredTableAssociationsInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListConfiguredTablesInputRequestTypeDef = TypedDict(
    "ListConfiguredTablesInputRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListMembersInputRequestTypeDef = TypedDict(
    "ListMembersInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListMembershipsInputRequestTypeDef = TypedDict(
    "ListMembershipsInputRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "status": NotRequired[MembershipStatusType],
    },
)
ListProtectedQueriesInputRequestTypeDef = TypedDict(
    "ListProtectedQueriesInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "status": NotRequired[ProtectedQueryStatusType],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ProtectedQuerySummaryTypeDef = TypedDict(
    "ProtectedQuerySummaryTypeDef",
    {
        "id": str,
        "membershipId": str,
        "membershipArn": str,
        "createTime": datetime,
        "status": ProtectedQueryStatusType,
    },
)
ListSchemasInputRequestTypeDef = TypedDict(
    "ListSchemasInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "schemaType": NotRequired[Literal["TABLE"]],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
SchemaSummaryTypeDef = TypedDict(
    "SchemaSummaryTypeDef",
    {
        "name": str,
        "type": Literal["TABLE"],
        "creatorAccountId": str,
        "createTime": datetime,
        "updateTime": datetime,
        "collaborationId": str,
        "collaborationArn": str,
        "analysisRuleTypes": List[AnalysisRuleTypeType],
        "analysisMethod": NotRequired[Literal["DIRECT_QUERY"]],
    },
)
ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
MembershipQueryComputePaymentConfigTypeDef = TypedDict(
    "MembershipQueryComputePaymentConfigTypeDef",
    {
        "isResponsible": bool,
    },
)
ProtectedQueryS3OutputConfigurationTypeDef = TypedDict(
    "ProtectedQueryS3OutputConfigurationTypeDef",
    {
        "resultFormat": ResultFormatType,
        "bucket": str,
        "keyPrefix": NotRequired[str],
    },
)
QueryComputePaymentConfigTypeDef = TypedDict(
    "QueryComputePaymentConfigTypeDef",
    {
        "isResponsible": bool,
    },
)
ProtectedQueryErrorTypeDef = TypedDict(
    "ProtectedQueryErrorTypeDef",
    {
        "message": str,
        "code": str,
    },
)
ProtectedQueryS3OutputTypeDef = TypedDict(
    "ProtectedQueryS3OutputTypeDef",
    {
        "location": str,
    },
)
ProtectedQuerySingleMemberOutputTypeDef = TypedDict(
    "ProtectedQuerySingleMemberOutputTypeDef",
    {
        "accountId": str,
    },
)
ProtectedQuerySQLParametersTypeDef = TypedDict(
    "ProtectedQuerySQLParametersTypeDef",
    {
        "queryString": NotRequired[str],
        "analysisTemplateArn": NotRequired[str],
        "parameters": NotRequired[Dict[str, str]],
    },
)
ProtectedQueryStatisticsTypeDef = TypedDict(
    "ProtectedQueryStatisticsTypeDef",
    {
        "totalDurationInMillis": NotRequired[int],
    },
)
TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)
UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
UpdateAnalysisTemplateInputRequestTypeDef = TypedDict(
    "UpdateAnalysisTemplateInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "analysisTemplateIdentifier": str,
        "description": NotRequired[str],
    },
)
UpdateCollaborationInputRequestTypeDef = TypedDict(
    "UpdateCollaborationInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
    },
)
UpdateConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "UpdateConfiguredTableAssociationInputRequestTypeDef",
    {
        "configuredTableAssociationIdentifier": str,
        "membershipIdentifier": str,
        "description": NotRequired[str],
        "roleArn": NotRequired[str],
    },
)
UpdateConfiguredTableInputRequestTypeDef = TypedDict(
    "UpdateConfiguredTableInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
    },
)
UpdateProtectedQueryInputRequestTypeDef = TypedDict(
    "UpdateProtectedQueryInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "protectedQueryIdentifier": str,
        "targetStatus": Literal["CANCELLED"],
    },
)
AnalysisRuleAggregationTypeDef = TypedDict(
    "AnalysisRuleAggregationTypeDef",
    {
        "aggregateColumns": Sequence[AggregateColumnTypeDef],
        "joinColumns": Sequence[str],
        "dimensionColumns": Sequence[str],
        "scalarFunctions": Sequence[ScalarFunctionsType],
        "outputConstraints": Sequence[AggregationConstraintTypeDef],
        "joinRequired": NotRequired[Literal["QUERY_RUNNER"]],
        "allowedJoinOperators": NotRequired[Sequence[JoinOperatorType]],
    },
)
AnalysisTemplateTypeDef = TypedDict(
    "AnalysisTemplateTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "membershipId": str,
        "membershipArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "schema": AnalysisSchemaTypeDef,
        "format": Literal["SQL"],
        "source": AnalysisSourceTypeDef,
        "description": NotRequired[str],
        "analysisParameters": NotRequired[List[AnalysisParameterTypeDef]],
    },
)
CollaborationAnalysisTemplateTypeDef = TypedDict(
    "CollaborationAnalysisTemplateTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "creatorAccountId": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "schema": AnalysisSchemaTypeDef,
        "format": Literal["SQL"],
        "source": AnalysisSourceTypeDef,
        "description": NotRequired[str],
        "analysisParameters": NotRequired[List[AnalysisParameterTypeDef]],
    },
)
CreateAnalysisTemplateInputRequestTypeDef = TypedDict(
    "CreateAnalysisTemplateInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "name": str,
        "format": Literal["SQL"],
        "source": AnalysisSourceTypeDef,
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "analysisParameters": NotRequired[Sequence[AnalysisParameterTypeDef]],
    },
)
ListAnalysisTemplatesOutputTypeDef = TypedDict(
    "ListAnalysisTemplatesOutputTypeDef",
    {
        "nextToken": str,
        "analysisTemplateSummaries": List[AnalysisTemplateSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListCollaborationAnalysisTemplatesOutputTypeDef = TypedDict(
    "ListCollaborationAnalysisTemplatesOutputTypeDef",
    {
        "nextToken": str,
        "collaborationAnalysisTemplateSummaries": List[CollaborationAnalysisTemplateSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListCollaborationsOutputTypeDef = TypedDict(
    "ListCollaborationsOutputTypeDef",
    {
        "nextToken": str,
        "collaborationList": List[CollaborationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CollaborationTypeDef = TypedDict(
    "CollaborationTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "creatorAccountId": str,
        "creatorDisplayName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "memberStatus": MemberStatusType,
        "queryLogStatus": CollaborationQueryLogStatusType,
        "description": NotRequired[str],
        "membershipId": NotRequired[str],
        "membershipArn": NotRequired[str],
        "dataEncryptionMetadata": NotRequired[DataEncryptionMetadataTypeDef],
    },
)
SchemaTypeDef = TypedDict(
    "SchemaTypeDef",
    {
        "columns": List[ColumnTypeDef],
        "partitionKeys": List[ColumnTypeDef],
        "analysisRuleTypes": List[AnalysisRuleTypeType],
        "creatorAccountId": str,
        "name": str,
        "collaborationId": str,
        "collaborationArn": str,
        "description": str,
        "createTime": datetime,
        "updateTime": datetime,
        "type": Literal["TABLE"],
        "analysisMethod": NotRequired[Literal["DIRECT_QUERY"]],
    },
)
ListConfiguredTableAssociationsOutputTypeDef = TypedDict(
    "ListConfiguredTableAssociationsOutputTypeDef",
    {
        "configuredTableAssociationSummaries": List[ConfiguredTableAssociationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateConfiguredTableAssociationOutputTypeDef = TypedDict(
    "CreateConfiguredTableAssociationOutputTypeDef",
    {
        "configuredTableAssociation": ConfiguredTableAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetConfiguredTableAssociationOutputTypeDef = TypedDict(
    "GetConfiguredTableAssociationOutputTypeDef",
    {
        "configuredTableAssociation": ConfiguredTableAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateConfiguredTableAssociationOutputTypeDef = TypedDict(
    "UpdateConfiguredTableAssociationOutputTypeDef",
    {
        "configuredTableAssociation": ConfiguredTableAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListConfiguredTablesOutputTypeDef = TypedDict(
    "ListConfiguredTablesOutputTypeDef",
    {
        "configuredTableSummaries": List[ConfiguredTableSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TableReferenceTypeDef = TypedDict(
    "TableReferenceTypeDef",
    {
        "glue": NotRequired[GlueTableReferenceTypeDef],
    },
)
ListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef = TypedDict(
    "ListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef",
    {
        "membershipIdentifier": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef = (
    TypedDict(
        "ListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef",
        {
            "collaborationIdentifier": str,
            "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
        },
    )
)
ListCollaborationsInputListCollaborationsPaginateTypeDef = TypedDict(
    "ListCollaborationsInputListCollaborationsPaginateTypeDef",
    {
        "memberStatus": NotRequired[FilterableMemberStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef = TypedDict(
    "ListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef",
    {
        "membershipIdentifier": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef = TypedDict(
    "ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListMembersInputListMembersPaginateTypeDef = TypedDict(
    "ListMembersInputListMembersPaginateTypeDef",
    {
        "collaborationIdentifier": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListMembershipsInputListMembershipsPaginateTypeDef = TypedDict(
    "ListMembershipsInputListMembershipsPaginateTypeDef",
    {
        "status": NotRequired[MembershipStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListProtectedQueriesInputListProtectedQueriesPaginateTypeDef = TypedDict(
    "ListProtectedQueriesInputListProtectedQueriesPaginateTypeDef",
    {
        "membershipIdentifier": str,
        "status": NotRequired[ProtectedQueryStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSchemasInputListSchemasPaginateTypeDef = TypedDict(
    "ListSchemasInputListSchemasPaginateTypeDef",
    {
        "collaborationIdentifier": str,
        "schemaType": NotRequired[Literal["TABLE"]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListProtectedQueriesOutputTypeDef = TypedDict(
    "ListProtectedQueriesOutputTypeDef",
    {
        "nextToken": str,
        "protectedQueries": List[ProtectedQuerySummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListSchemasOutputTypeDef = TypedDict(
    "ListSchemasOutputTypeDef",
    {
        "schemaSummaries": List[SchemaSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
MembershipPaymentConfigurationTypeDef = TypedDict(
    "MembershipPaymentConfigurationTypeDef",
    {
        "queryCompute": MembershipQueryComputePaymentConfigTypeDef,
    },
)
MembershipProtectedQueryOutputConfigurationTypeDef = TypedDict(
    "MembershipProtectedQueryOutputConfigurationTypeDef",
    {
        "s3": NotRequired[ProtectedQueryS3OutputConfigurationTypeDef],
    },
)
ProtectedQueryOutputConfigurationTypeDef = TypedDict(
    "ProtectedQueryOutputConfigurationTypeDef",
    {
        "s3": NotRequired[ProtectedQueryS3OutputConfigurationTypeDef],
    },
)
PaymentConfigurationTypeDef = TypedDict(
    "PaymentConfigurationTypeDef",
    {
        "queryCompute": QueryComputePaymentConfigTypeDef,
    },
)
ProtectedQueryOutputTypeDef = TypedDict(
    "ProtectedQueryOutputTypeDef",
    {
        "s3": NotRequired[ProtectedQueryS3OutputTypeDef],
        "memberList": NotRequired[List[ProtectedQuerySingleMemberOutputTypeDef]],
    },
)
AnalysisRulePolicyV1TypeDef = TypedDict(
    "AnalysisRulePolicyV1TypeDef",
    {
        "list": NotRequired[AnalysisRuleListTypeDef],
        "aggregation": NotRequired[AnalysisRuleAggregationTypeDef],
        "custom": NotRequired[AnalysisRuleCustomTypeDef],
    },
)
ConfiguredTableAnalysisRulePolicyV1TypeDef = TypedDict(
    "ConfiguredTableAnalysisRulePolicyV1TypeDef",
    {
        "list": NotRequired[AnalysisRuleListTypeDef],
        "aggregation": NotRequired[AnalysisRuleAggregationTypeDef],
        "custom": NotRequired[AnalysisRuleCustomTypeDef],
    },
)
CreateAnalysisTemplateOutputTypeDef = TypedDict(
    "CreateAnalysisTemplateOutputTypeDef",
    {
        "analysisTemplate": AnalysisTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAnalysisTemplateOutputTypeDef = TypedDict(
    "GetAnalysisTemplateOutputTypeDef",
    {
        "analysisTemplate": AnalysisTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAnalysisTemplateOutputTypeDef = TypedDict(
    "UpdateAnalysisTemplateOutputTypeDef",
    {
        "analysisTemplate": AnalysisTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchGetCollaborationAnalysisTemplateOutputTypeDef = TypedDict(
    "BatchGetCollaborationAnalysisTemplateOutputTypeDef",
    {
        "collaborationAnalysisTemplates": List[CollaborationAnalysisTemplateTypeDef],
        "errors": List[BatchGetCollaborationAnalysisTemplateErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetCollaborationAnalysisTemplateOutputTypeDef = TypedDict(
    "GetCollaborationAnalysisTemplateOutputTypeDef",
    {
        "collaborationAnalysisTemplate": CollaborationAnalysisTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateCollaborationOutputTypeDef = TypedDict(
    "CreateCollaborationOutputTypeDef",
    {
        "collaboration": CollaborationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetCollaborationOutputTypeDef = TypedDict(
    "GetCollaborationOutputTypeDef",
    {
        "collaboration": CollaborationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateCollaborationOutputTypeDef = TypedDict(
    "UpdateCollaborationOutputTypeDef",
    {
        "collaboration": CollaborationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchGetSchemaOutputTypeDef = TypedDict(
    "BatchGetSchemaOutputTypeDef",
    {
        "schemas": List[SchemaTypeDef],
        "errors": List[BatchGetSchemaErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSchemaOutputTypeDef = TypedDict(
    "GetSchemaOutputTypeDef",
    {
        "schema": SchemaTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ConfiguredTableTypeDef = TypedDict(
    "ConfiguredTableTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "tableReference": TableReferenceTypeDef,
        "createTime": datetime,
        "updateTime": datetime,
        "analysisRuleTypes": List[ConfiguredTableAnalysisRuleTypeType],
        "analysisMethod": Literal["DIRECT_QUERY"],
        "allowedColumns": List[str],
        "description": NotRequired[str],
    },
)
CreateConfiguredTableInputRequestTypeDef = TypedDict(
    "CreateConfiguredTableInputRequestTypeDef",
    {
        "name": str,
        "tableReference": TableReferenceTypeDef,
        "allowedColumns": Sequence[str],
        "analysisMethod": Literal["DIRECT_QUERY"],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
MembershipSummaryTypeDef = TypedDict(
    "MembershipSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationArn": str,
        "collaborationId": str,
        "collaborationCreatorAccountId": str,
        "collaborationCreatorDisplayName": str,
        "collaborationName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "status": MembershipStatusType,
        "memberAbilities": List[MemberAbilityType],
        "paymentConfiguration": MembershipPaymentConfigurationTypeDef,
    },
)
MembershipProtectedQueryResultConfigurationTypeDef = TypedDict(
    "MembershipProtectedQueryResultConfigurationTypeDef",
    {
        "outputConfiguration": MembershipProtectedQueryOutputConfigurationTypeDef,
        "roleArn": NotRequired[str],
    },
)
ProtectedQueryResultConfigurationTypeDef = TypedDict(
    "ProtectedQueryResultConfigurationTypeDef",
    {
        "outputConfiguration": ProtectedQueryOutputConfigurationTypeDef,
    },
)
MemberSpecificationTypeDef = TypedDict(
    "MemberSpecificationTypeDef",
    {
        "accountId": str,
        "memberAbilities": Sequence[MemberAbilityType],
        "displayName": str,
        "paymentConfiguration": NotRequired[PaymentConfigurationTypeDef],
    },
)
MemberSummaryTypeDef = TypedDict(
    "MemberSummaryTypeDef",
    {
        "accountId": str,
        "status": MemberStatusType,
        "displayName": str,
        "abilities": List[MemberAbilityType],
        "createTime": datetime,
        "updateTime": datetime,
        "paymentConfiguration": PaymentConfigurationTypeDef,
        "membershipId": NotRequired[str],
        "membershipArn": NotRequired[str],
    },
)
ProtectedQueryResultTypeDef = TypedDict(
    "ProtectedQueryResultTypeDef",
    {
        "output": ProtectedQueryOutputTypeDef,
    },
)
AnalysisRulePolicyTypeDef = TypedDict(
    "AnalysisRulePolicyTypeDef",
    {
        "v1": NotRequired[AnalysisRulePolicyV1TypeDef],
    },
)
ConfiguredTableAnalysisRulePolicyTypeDef = TypedDict(
    "ConfiguredTableAnalysisRulePolicyTypeDef",
    {
        "v1": NotRequired[ConfiguredTableAnalysisRulePolicyV1TypeDef],
    },
)
CreateConfiguredTableOutputTypeDef = TypedDict(
    "CreateConfiguredTableOutputTypeDef",
    {
        "configuredTable": ConfiguredTableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetConfiguredTableOutputTypeDef = TypedDict(
    "GetConfiguredTableOutputTypeDef",
    {
        "configuredTable": ConfiguredTableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateConfiguredTableOutputTypeDef = TypedDict(
    "UpdateConfiguredTableOutputTypeDef",
    {
        "configuredTable": ConfiguredTableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListMembershipsOutputTypeDef = TypedDict(
    "ListMembershipsOutputTypeDef",
    {
        "nextToken": str,
        "membershipSummaries": List[MembershipSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateMembershipInputRequestTypeDef = TypedDict(
    "CreateMembershipInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "queryLogStatus": MembershipQueryLogStatusType,
        "tags": NotRequired[Mapping[str, str]],
        "defaultResultConfiguration": NotRequired[
            MembershipProtectedQueryResultConfigurationTypeDef
        ],
        "paymentConfiguration": NotRequired[MembershipPaymentConfigurationTypeDef],
    },
)
MembershipTypeDef = TypedDict(
    "MembershipTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationArn": str,
        "collaborationId": str,
        "collaborationCreatorAccountId": str,
        "collaborationCreatorDisplayName": str,
        "collaborationName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "status": MembershipStatusType,
        "memberAbilities": List[MemberAbilityType],
        "queryLogStatus": MembershipQueryLogStatusType,
        "paymentConfiguration": MembershipPaymentConfigurationTypeDef,
        "defaultResultConfiguration": NotRequired[
            MembershipProtectedQueryResultConfigurationTypeDef
        ],
    },
)
UpdateMembershipInputRequestTypeDef = TypedDict(
    "UpdateMembershipInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "queryLogStatus": NotRequired[MembershipQueryLogStatusType],
        "defaultResultConfiguration": NotRequired[
            MembershipProtectedQueryResultConfigurationTypeDef
        ],
    },
)
StartProtectedQueryInputRequestTypeDef = TypedDict(
    "StartProtectedQueryInputRequestTypeDef",
    {
        "type": Literal["SQL"],
        "membershipIdentifier": str,
        "sqlParameters": ProtectedQuerySQLParametersTypeDef,
        "resultConfiguration": NotRequired[ProtectedQueryResultConfigurationTypeDef],
    },
)
CreateCollaborationInputRequestTypeDef = TypedDict(
    "CreateCollaborationInputRequestTypeDef",
    {
        "members": Sequence[MemberSpecificationTypeDef],
        "name": str,
        "description": str,
        "creatorMemberAbilities": Sequence[MemberAbilityType],
        "creatorDisplayName": str,
        "queryLogStatus": CollaborationQueryLogStatusType,
        "dataEncryptionMetadata": NotRequired[DataEncryptionMetadataTypeDef],
        "tags": NotRequired[Mapping[str, str]],
        "creatorPaymentConfiguration": NotRequired[PaymentConfigurationTypeDef],
    },
)
ListMembersOutputTypeDef = TypedDict(
    "ListMembersOutputTypeDef",
    {
        "nextToken": str,
        "memberSummaries": List[MemberSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ProtectedQueryTypeDef = TypedDict(
    "ProtectedQueryTypeDef",
    {
        "id": str,
        "membershipId": str,
        "membershipArn": str,
        "createTime": datetime,
        "status": ProtectedQueryStatusType,
        "sqlParameters": NotRequired[ProtectedQuerySQLParametersTypeDef],
        "resultConfiguration": NotRequired[ProtectedQueryResultConfigurationTypeDef],
        "statistics": NotRequired[ProtectedQueryStatisticsTypeDef],
        "result": NotRequired[ProtectedQueryResultTypeDef],
        "error": NotRequired[ProtectedQueryErrorTypeDef],
    },
)
AnalysisRuleTypeDef = TypedDict(
    "AnalysisRuleTypeDef",
    {
        "collaborationId": str,
        "type": AnalysisRuleTypeType,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "policy": AnalysisRulePolicyTypeDef,
    },
)
ConfiguredTableAnalysisRuleTypeDef = TypedDict(
    "ConfiguredTableAnalysisRuleTypeDef",
    {
        "configuredTableId": str,
        "configuredTableArn": str,
        "policy": ConfiguredTableAnalysisRulePolicyTypeDef,
        "type": ConfiguredTableAnalysisRuleTypeType,
        "createTime": datetime,
        "updateTime": datetime,
    },
)
CreateConfiguredTableAnalysisRuleInputRequestTypeDef = TypedDict(
    "CreateConfiguredTableAnalysisRuleInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
        "analysisRuleType": ConfiguredTableAnalysisRuleTypeType,
        "analysisRulePolicy": ConfiguredTableAnalysisRulePolicyTypeDef,
    },
)
UpdateConfiguredTableAnalysisRuleInputRequestTypeDef = TypedDict(
    "UpdateConfiguredTableAnalysisRuleInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
        "analysisRuleType": ConfiguredTableAnalysisRuleTypeType,
        "analysisRulePolicy": ConfiguredTableAnalysisRulePolicyTypeDef,
    },
)
CreateMembershipOutputTypeDef = TypedDict(
    "CreateMembershipOutputTypeDef",
    {
        "membership": MembershipTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMembershipOutputTypeDef = TypedDict(
    "GetMembershipOutputTypeDef",
    {
        "membership": MembershipTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateMembershipOutputTypeDef = TypedDict(
    "UpdateMembershipOutputTypeDef",
    {
        "membership": MembershipTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetProtectedQueryOutputTypeDef = TypedDict(
    "GetProtectedQueryOutputTypeDef",
    {
        "protectedQuery": ProtectedQueryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartProtectedQueryOutputTypeDef = TypedDict(
    "StartProtectedQueryOutputTypeDef",
    {
        "protectedQuery": ProtectedQueryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateProtectedQueryOutputTypeDef = TypedDict(
    "UpdateProtectedQueryOutputTypeDef",
    {
        "protectedQuery": ProtectedQueryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSchemaAnalysisRuleOutputTypeDef = TypedDict(
    "GetSchemaAnalysisRuleOutputTypeDef",
    {
        "analysisRule": AnalysisRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateConfiguredTableAnalysisRuleOutputTypeDef = TypedDict(
    "CreateConfiguredTableAnalysisRuleOutputTypeDef",
    {
        "analysisRule": ConfiguredTableAnalysisRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetConfiguredTableAnalysisRuleOutputTypeDef = TypedDict(
    "GetConfiguredTableAnalysisRuleOutputTypeDef",
    {
        "analysisRule": ConfiguredTableAnalysisRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateConfiguredTableAnalysisRuleOutputTypeDef = TypedDict(
    "UpdateConfiguredTableAnalysisRuleOutputTypeDef",
    {
        "analysisRule": ConfiguredTableAnalysisRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
