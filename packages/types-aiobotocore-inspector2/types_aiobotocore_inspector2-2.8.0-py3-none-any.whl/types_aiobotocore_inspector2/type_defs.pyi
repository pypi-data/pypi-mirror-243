"""
Type annotations for inspector2 service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/type_defs/)

Usage::

    ```python
    from types_aiobotocore_inspector2.type_defs import SeverityCountsTypeDef

    data: SeverityCountsTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccountSortByType,
    AggregationFindingTypeType,
    AggregationResourceTypeType,
    AggregationTypeType,
    AmiSortByType,
    ArchitectureType,
    AwsEcrContainerSortByType,
    CodeSnippetErrorCodeType,
    CoverageResourceTypeType,
    CoverageStringComparisonType,
    DelegatedAdminStatusType,
    Ec2DeepInspectionStatusType,
    Ec2InstanceSortByType,
    Ec2PlatformType,
    EcrRescanDurationStatusType,
    EcrRescanDurationType,
    EcrScanFrequencyType,
    ErrorCodeType,
    ExploitAvailableType,
    ExternalReportStatusType,
    FilterActionType,
    FindingDetailsErrorCodeType,
    FindingStatusType,
    FindingTypeSortByType,
    FindingTypeType,
    FixAvailableType,
    FreeTrialInfoErrorCodeType,
    FreeTrialStatusType,
    FreeTrialTypeType,
    GroupKeyType,
    ImageLayerSortByType,
    LambdaFunctionSortByType,
    LambdaLayerSortByType,
    NetworkProtocolType,
    OperationType,
    PackageManagerType,
    PackageSortByType,
    PackageTypeType,
    RelationshipStatusType,
    ReportFormatType,
    ReportingErrorCodeType,
    RepositorySortByType,
    ResourceScanTypeType,
    ResourceStringComparisonType,
    ResourceTypeType,
    RuntimeType,
    SbomReportFormatType,
    ScanStatusCodeType,
    ScanStatusReasonType,
    ScanTypeType,
    ServiceType,
    SeverityType,
    SortFieldType,
    SortOrderType,
    StatusType,
    StringComparisonType,
    TitleSortByType,
    UsageTypeType,
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
    "SeverityCountsTypeDef",
    "AccountAggregationTypeDef",
    "StateTypeDef",
    "ResourceStatusTypeDef",
    "FindingTypeAggregationTypeDef",
    "StringFilterTypeDef",
    "AssociateMemberRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AtigDataTypeDef",
    "AutoEnableTypeDef",
    "AwsEc2InstanceDetailsTypeDef",
    "AwsEcrContainerImageDetailsTypeDef",
    "LambdaVpcConfigTypeDef",
    "BatchGetAccountStatusRequestRequestTypeDef",
    "BatchGetCodeSnippetRequestRequestTypeDef",
    "CodeSnippetErrorTypeDef",
    "BatchGetFindingDetailsRequestRequestTypeDef",
    "FindingDetailsErrorTypeDef",
    "BatchGetFreeTrialInfoRequestRequestTypeDef",
    "FreeTrialInfoErrorTypeDef",
    "BatchGetMemberEc2DeepInspectionStatusRequestRequestTypeDef",
    "FailedMemberAccountEc2DeepInspectionStatusStateTypeDef",
    "MemberAccountEc2DeepInspectionStatusStateTypeDef",
    "MemberAccountEc2DeepInspectionStatusTypeDef",
    "CancelFindingsReportRequestRequestTypeDef",
    "CancelSbomExportRequestRequestTypeDef",
    "CisaDataTypeDef",
    "CodeFilePathTypeDef",
    "CodeLineTypeDef",
    "SuggestedFixTypeDef",
    "CountsTypeDef",
    "TimestampTypeDef",
    "CoverageMapFilterTypeDef",
    "CoverageStringFilterTypeDef",
    "ScanStatusTypeDef",
    "DestinationTypeDef",
    "Cvss2TypeDef",
    "Cvss3TypeDef",
    "CvssScoreAdjustmentTypeDef",
    "CvssScoreTypeDef",
    "DateFilterPaginatorTypeDef",
    "DelegatedAdminAccountTypeDef",
    "DelegatedAdminTypeDef",
    "DeleteFilterRequestRequestTypeDef",
    "DisableDelegatedAdminAccountRequestRequestTypeDef",
    "DisableRequestRequestTypeDef",
    "DisassociateMemberRequestRequestTypeDef",
    "MapFilterTypeDef",
    "Ec2MetadataTypeDef",
    "EcrRescanDurationStateTypeDef",
    "EcrConfigurationTypeDef",
    "EcrContainerImageMetadataTypeDef",
    "EcrRepositoryMetadataTypeDef",
    "EnableDelegatedAdminAccountRequestRequestTypeDef",
    "EnableRequestRequestTypeDef",
    "EpssDetailsTypeDef",
    "EpssTypeDef",
    "EvidenceTypeDef",
    "ExploitObservedTypeDef",
    "ExploitabilityDetailsTypeDef",
    "NumberFilterTypeDef",
    "PortRangeFilterTypeDef",
    "FreeTrialInfoTypeDef",
    "GetEncryptionKeyRequestRequestTypeDef",
    "GetFindingsReportStatusRequestRequestTypeDef",
    "GetMemberRequestRequestTypeDef",
    "MemberTypeDef",
    "GetSbomExportRequestRequestTypeDef",
    "LambdaFunctionMetadataTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccountPermissionsRequestRequestTypeDef",
    "PermissionTypeDef",
    "ListDelegatedAdminAccountsRequestRequestTypeDef",
    "ListFiltersRequestRequestTypeDef",
    "SortCriteriaTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListUsageTotalsRequestRequestTypeDef",
    "StepTypeDef",
    "PortRangeTypeDef",
    "VulnerablePackageTypeDef",
    "RecommendationTypeDef",
    "ResetEncryptionKeyRequestRequestTypeDef",
    "ResourceMapFilterTypeDef",
    "ResourceStringFilterTypeDef",
    "SearchVulnerabilitiesFilterCriteriaTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateEc2DeepInspectionConfigurationRequestRequestTypeDef",
    "UpdateEncryptionKeyRequestRequestTypeDef",
    "UpdateOrgEc2DeepInspectionConfigurationRequestRequestTypeDef",
    "UsageTypeDef",
    "AccountAggregationResponseTypeDef",
    "AmiAggregationResponseTypeDef",
    "AwsEcrContainerAggregationResponseTypeDef",
    "Ec2InstanceAggregationResponseTypeDef",
    "FindingTypeAggregationResponseTypeDef",
    "ImageLayerAggregationResponseTypeDef",
    "LambdaFunctionAggregationResponseTypeDef",
    "LambdaLayerAggregationResponseTypeDef",
    "PackageAggregationResponseTypeDef",
    "RepositoryAggregationResponseTypeDef",
    "TitleAggregationResponseTypeDef",
    "ResourceStateTypeDef",
    "AccountTypeDef",
    "FailedAccountTypeDef",
    "AmiAggregationTypeDef",
    "AwsEcrContainerAggregationTypeDef",
    "ImageLayerAggregationTypeDef",
    "LambdaLayerAggregationTypeDef",
    "PackageAggregationTypeDef",
    "RepositoryAggregationTypeDef",
    "TitleAggregationTypeDef",
    "AssociateMemberResponseTypeDef",
    "CancelFindingsReportResponseTypeDef",
    "CancelSbomExportResponseTypeDef",
    "CreateFilterResponseTypeDef",
    "CreateFindingsReportResponseTypeDef",
    "CreateSbomExportResponseTypeDef",
    "DeleteFilterResponseTypeDef",
    "DisableDelegatedAdminAccountResponseTypeDef",
    "DisassociateMemberResponseTypeDef",
    "EnableDelegatedAdminAccountResponseTypeDef",
    "GetEc2DeepInspectionConfigurationResponseTypeDef",
    "GetEncryptionKeyResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateEc2DeepInspectionConfigurationResponseTypeDef",
    "UpdateFilterResponseTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    "UpdateOrganizationConfigurationResponseTypeDef",
    "AwsLambdaFunctionDetailsTypeDef",
    "BatchGetMemberEc2DeepInspectionStatusResponseTypeDef",
    "BatchUpdateMemberEc2DeepInspectionStatusResponseTypeDef",
    "BatchUpdateMemberEc2DeepInspectionStatusRequestRequestTypeDef",
    "CodeVulnerabilityDetailsTypeDef",
    "CodeSnippetResultTypeDef",
    "ListCoverageStatisticsResponseTypeDef",
    "CoverageDateFilterTypeDef",
    "DateFilterTypeDef",
    "CvssScoreDetailsTypeDef",
    "ListDelegatedAdminAccountsResponseTypeDef",
    "GetDelegatedAdminAccountResponseTypeDef",
    "Ec2InstanceAggregationTypeDef",
    "LambdaFunctionAggregationTypeDef",
    "EcrConfigurationStateTypeDef",
    "UpdateConfigurationRequestRequestTypeDef",
    "FindingDetailTypeDef",
    "VulnerabilityTypeDef",
    "PackageFilterTypeDef",
    "FreeTrialAccountInfoTypeDef",
    "GetMemberResponseTypeDef",
    "ListMembersResponseTypeDef",
    "ResourceScanMetadataTypeDef",
    "ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef",
    "ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef",
    "ListFiltersRequestListFiltersPaginateTypeDef",
    "ListMembersRequestListMembersPaginateTypeDef",
    "ListUsageTotalsRequestListUsageTotalsPaginateTypeDef",
    "ListAccountPermissionsResponseTypeDef",
    "NetworkPathTypeDef",
    "PackageVulnerabilityDetailsTypeDef",
    "RemediationTypeDef",
    "ResourceFilterCriteriaTypeDef",
    "SearchVulnerabilitiesRequestRequestTypeDef",
    "SearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef",
    "UsageTotalTypeDef",
    "AggregationResponseTypeDef",
    "AccountStateTypeDef",
    "DisableResponseTypeDef",
    "EnableResponseTypeDef",
    "ResourceDetailsTypeDef",
    "BatchGetCodeSnippetResponseTypeDef",
    "CoverageFilterCriteriaTypeDef",
    "InspectorScoreDetailsTypeDef",
    "AggregationRequestTypeDef",
    "GetConfigurationResponseTypeDef",
    "BatchGetFindingDetailsResponseTypeDef",
    "SearchVulnerabilitiesResponseTypeDef",
    "FilterCriteriaPaginatorTypeDef",
    "FilterCriteriaTypeDef",
    "BatchGetFreeTrialInfoResponseTypeDef",
    "CoveredResourceTypeDef",
    "NetworkReachabilityDetailsTypeDef",
    "CreateSbomExportRequestRequestTypeDef",
    "GetSbomExportResponseTypeDef",
    "ListUsageTotalsResponseTypeDef",
    "ListFindingAggregationsResponseTypeDef",
    "BatchGetAccountStatusResponseTypeDef",
    "ResourceTypeDef",
    "ListCoverageRequestListCoveragePaginateTypeDef",
    "ListCoverageRequestRequestTypeDef",
    "ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef",
    "ListCoverageStatisticsRequestRequestTypeDef",
    "ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    "ListFindingAggregationsRequestRequestTypeDef",
    "FilterPaginatorTypeDef",
    "ListFindingsRequestListFindingsPaginateTypeDef",
    "CreateFilterRequestRequestTypeDef",
    "CreateFindingsReportRequestRequestTypeDef",
    "FilterTypeDef",
    "GetFindingsReportStatusResponseTypeDef",
    "ListFindingsRequestRequestTypeDef",
    "UpdateFilterRequestRequestTypeDef",
    "ListCoverageResponseTypeDef",
    "FindingTypeDef",
    "ListFiltersResponsePaginatorTypeDef",
    "ListFiltersResponseTypeDef",
    "ListFindingsResponseTypeDef",
)

SeverityCountsTypeDef = TypedDict(
    "SeverityCountsTypeDef",
    {
        "all": NotRequired[int],
        "critical": NotRequired[int],
        "high": NotRequired[int],
        "medium": NotRequired[int],
    },
)
AccountAggregationTypeDef = TypedDict(
    "AccountAggregationTypeDef",
    {
        "findingType": NotRequired[AggregationFindingTypeType],
        "resourceType": NotRequired[AggregationResourceTypeType],
        "sortBy": NotRequired[AccountSortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
StateTypeDef = TypedDict(
    "StateTypeDef",
    {
        "errorCode": ErrorCodeType,
        "errorMessage": str,
        "status": StatusType,
    },
)
ResourceStatusTypeDef = TypedDict(
    "ResourceStatusTypeDef",
    {
        "ec2": StatusType,
        "ecr": StatusType,
        "lambda": NotRequired[StatusType],
        "lambdaCode": NotRequired[StatusType],
    },
)
FindingTypeAggregationTypeDef = TypedDict(
    "FindingTypeAggregationTypeDef",
    {
        "findingType": NotRequired[AggregationFindingTypeType],
        "resourceType": NotRequired[AggregationResourceTypeType],
        "sortBy": NotRequired[FindingTypeSortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
StringFilterTypeDef = TypedDict(
    "StringFilterTypeDef",
    {
        "comparison": StringComparisonType,
        "value": str,
    },
)
AssociateMemberRequestRequestTypeDef = TypedDict(
    "AssociateMemberRequestRequestTypeDef",
    {
        "accountId": str,
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
AtigDataTypeDef = TypedDict(
    "AtigDataTypeDef",
    {
        "firstSeen": NotRequired[datetime],
        "lastSeen": NotRequired[datetime],
        "targets": NotRequired[List[str]],
        "ttps": NotRequired[List[str]],
    },
)
AutoEnableTypeDef = TypedDict(
    "AutoEnableTypeDef",
    {
        "ec2": bool,
        "ecr": bool,
        "lambda": NotRequired[bool],
        "lambdaCode": NotRequired[bool],
    },
)
AwsEc2InstanceDetailsTypeDef = TypedDict(
    "AwsEc2InstanceDetailsTypeDef",
    {
        "iamInstanceProfileArn": NotRequired[str],
        "imageId": NotRequired[str],
        "ipV4Addresses": NotRequired[List[str]],
        "ipV6Addresses": NotRequired[List[str]],
        "keyName": NotRequired[str],
        "launchedAt": NotRequired[datetime],
        "platform": NotRequired[str],
        "subnetId": NotRequired[str],
        "type": NotRequired[str],
        "vpcId": NotRequired[str],
    },
)
AwsEcrContainerImageDetailsTypeDef = TypedDict(
    "AwsEcrContainerImageDetailsTypeDef",
    {
        "imageHash": str,
        "registry": str,
        "repositoryName": str,
        "architecture": NotRequired[str],
        "author": NotRequired[str],
        "imageTags": NotRequired[List[str]],
        "platform": NotRequired[str],
        "pushedAt": NotRequired[datetime],
    },
)
LambdaVpcConfigTypeDef = TypedDict(
    "LambdaVpcConfigTypeDef",
    {
        "securityGroupIds": NotRequired[List[str]],
        "subnetIds": NotRequired[List[str]],
        "vpcId": NotRequired[str],
    },
)
BatchGetAccountStatusRequestRequestTypeDef = TypedDict(
    "BatchGetAccountStatusRequestRequestTypeDef",
    {
        "accountIds": NotRequired[Sequence[str]],
    },
)
BatchGetCodeSnippetRequestRequestTypeDef = TypedDict(
    "BatchGetCodeSnippetRequestRequestTypeDef",
    {
        "findingArns": Sequence[str],
    },
)
CodeSnippetErrorTypeDef = TypedDict(
    "CodeSnippetErrorTypeDef",
    {
        "errorCode": CodeSnippetErrorCodeType,
        "errorMessage": str,
        "findingArn": str,
    },
)
BatchGetFindingDetailsRequestRequestTypeDef = TypedDict(
    "BatchGetFindingDetailsRequestRequestTypeDef",
    {
        "findingArns": Sequence[str],
    },
)
FindingDetailsErrorTypeDef = TypedDict(
    "FindingDetailsErrorTypeDef",
    {
        "errorCode": FindingDetailsErrorCodeType,
        "errorMessage": str,
        "findingArn": str,
    },
)
BatchGetFreeTrialInfoRequestRequestTypeDef = TypedDict(
    "BatchGetFreeTrialInfoRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
    },
)
FreeTrialInfoErrorTypeDef = TypedDict(
    "FreeTrialInfoErrorTypeDef",
    {
        "accountId": str,
        "code": FreeTrialInfoErrorCodeType,
        "message": str,
    },
)
BatchGetMemberEc2DeepInspectionStatusRequestRequestTypeDef = TypedDict(
    "BatchGetMemberEc2DeepInspectionStatusRequestRequestTypeDef",
    {
        "accountIds": NotRequired[Sequence[str]],
    },
)
FailedMemberAccountEc2DeepInspectionStatusStateTypeDef = TypedDict(
    "FailedMemberAccountEc2DeepInspectionStatusStateTypeDef",
    {
        "accountId": str,
        "ec2ScanStatus": NotRequired[StatusType],
        "errorMessage": NotRequired[str],
    },
)
MemberAccountEc2DeepInspectionStatusStateTypeDef = TypedDict(
    "MemberAccountEc2DeepInspectionStatusStateTypeDef",
    {
        "accountId": str,
        "errorMessage": NotRequired[str],
        "status": NotRequired[Ec2DeepInspectionStatusType],
    },
)
MemberAccountEc2DeepInspectionStatusTypeDef = TypedDict(
    "MemberAccountEc2DeepInspectionStatusTypeDef",
    {
        "accountId": str,
        "activateDeepInspection": bool,
    },
)
CancelFindingsReportRequestRequestTypeDef = TypedDict(
    "CancelFindingsReportRequestRequestTypeDef",
    {
        "reportId": str,
    },
)
CancelSbomExportRequestRequestTypeDef = TypedDict(
    "CancelSbomExportRequestRequestTypeDef",
    {
        "reportId": str,
    },
)
CisaDataTypeDef = TypedDict(
    "CisaDataTypeDef",
    {
        "action": NotRequired[str],
        "dateAdded": NotRequired[datetime],
        "dateDue": NotRequired[datetime],
    },
)
CodeFilePathTypeDef = TypedDict(
    "CodeFilePathTypeDef",
    {
        "endLine": int,
        "fileName": str,
        "filePath": str,
        "startLine": int,
    },
)
CodeLineTypeDef = TypedDict(
    "CodeLineTypeDef",
    {
        "content": str,
        "lineNumber": int,
    },
)
SuggestedFixTypeDef = TypedDict(
    "SuggestedFixTypeDef",
    {
        "code": NotRequired[str],
        "description": NotRequired[str],
    },
)
CountsTypeDef = TypedDict(
    "CountsTypeDef",
    {
        "count": NotRequired[int],
        "groupKey": NotRequired[GroupKeyType],
    },
)
TimestampTypeDef = Union[datetime, str]
CoverageMapFilterTypeDef = TypedDict(
    "CoverageMapFilterTypeDef",
    {
        "comparison": Literal["EQUALS"],
        "key": str,
        "value": NotRequired[str],
    },
)
CoverageStringFilterTypeDef = TypedDict(
    "CoverageStringFilterTypeDef",
    {
        "comparison": CoverageStringComparisonType,
        "value": str,
    },
)
ScanStatusTypeDef = TypedDict(
    "ScanStatusTypeDef",
    {
        "reason": ScanStatusReasonType,
        "statusCode": ScanStatusCodeType,
    },
)
DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "bucketName": str,
        "kmsKeyArn": str,
        "keyPrefix": NotRequired[str],
    },
)
Cvss2TypeDef = TypedDict(
    "Cvss2TypeDef",
    {
        "baseScore": NotRequired[float],
        "scoringVector": NotRequired[str],
    },
)
Cvss3TypeDef = TypedDict(
    "Cvss3TypeDef",
    {
        "baseScore": NotRequired[float],
        "scoringVector": NotRequired[str],
    },
)
CvssScoreAdjustmentTypeDef = TypedDict(
    "CvssScoreAdjustmentTypeDef",
    {
        "metric": str,
        "reason": str,
    },
)
CvssScoreTypeDef = TypedDict(
    "CvssScoreTypeDef",
    {
        "baseScore": float,
        "scoringVector": str,
        "source": str,
        "version": str,
    },
)
DateFilterPaginatorTypeDef = TypedDict(
    "DateFilterPaginatorTypeDef",
    {
        "endInclusive": NotRequired[datetime],
        "startInclusive": NotRequired[datetime],
    },
)
DelegatedAdminAccountTypeDef = TypedDict(
    "DelegatedAdminAccountTypeDef",
    {
        "accountId": NotRequired[str],
        "status": NotRequired[DelegatedAdminStatusType],
    },
)
DelegatedAdminTypeDef = TypedDict(
    "DelegatedAdminTypeDef",
    {
        "accountId": NotRequired[str],
        "relationshipStatus": NotRequired[RelationshipStatusType],
    },
)
DeleteFilterRequestRequestTypeDef = TypedDict(
    "DeleteFilterRequestRequestTypeDef",
    {
        "arn": str,
    },
)
DisableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "DisableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "delegatedAdminAccountId": str,
    },
)
DisableRequestRequestTypeDef = TypedDict(
    "DisableRequestRequestTypeDef",
    {
        "accountIds": NotRequired[Sequence[str]],
        "resourceTypes": NotRequired[Sequence[ResourceScanTypeType]],
    },
)
DisassociateMemberRequestRequestTypeDef = TypedDict(
    "DisassociateMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)
MapFilterTypeDef = TypedDict(
    "MapFilterTypeDef",
    {
        "comparison": Literal["EQUALS"],
        "key": str,
        "value": NotRequired[str],
    },
)
Ec2MetadataTypeDef = TypedDict(
    "Ec2MetadataTypeDef",
    {
        "amiId": NotRequired[str],
        "platform": NotRequired[Ec2PlatformType],
        "tags": NotRequired[Dict[str, str]],
    },
)
EcrRescanDurationStateTypeDef = TypedDict(
    "EcrRescanDurationStateTypeDef",
    {
        "rescanDuration": NotRequired[EcrRescanDurationType],
        "status": NotRequired[EcrRescanDurationStatusType],
        "updatedAt": NotRequired[datetime],
    },
)
EcrConfigurationTypeDef = TypedDict(
    "EcrConfigurationTypeDef",
    {
        "rescanDuration": EcrRescanDurationType,
    },
)
EcrContainerImageMetadataTypeDef = TypedDict(
    "EcrContainerImageMetadataTypeDef",
    {
        "tags": NotRequired[List[str]],
    },
)
EcrRepositoryMetadataTypeDef = TypedDict(
    "EcrRepositoryMetadataTypeDef",
    {
        "name": NotRequired[str],
        "scanFrequency": NotRequired[EcrScanFrequencyType],
    },
)
EnableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "EnableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "delegatedAdminAccountId": str,
        "clientToken": NotRequired[str],
    },
)
EnableRequestRequestTypeDef = TypedDict(
    "EnableRequestRequestTypeDef",
    {
        "resourceTypes": Sequence[ResourceScanTypeType],
        "accountIds": NotRequired[Sequence[str]],
        "clientToken": NotRequired[str],
    },
)
EpssDetailsTypeDef = TypedDict(
    "EpssDetailsTypeDef",
    {
        "score": NotRequired[float],
    },
)
EpssTypeDef = TypedDict(
    "EpssTypeDef",
    {
        "score": NotRequired[float],
    },
)
EvidenceTypeDef = TypedDict(
    "EvidenceTypeDef",
    {
        "evidenceDetail": NotRequired[str],
        "evidenceRule": NotRequired[str],
        "severity": NotRequired[str],
    },
)
ExploitObservedTypeDef = TypedDict(
    "ExploitObservedTypeDef",
    {
        "firstSeen": NotRequired[datetime],
        "lastSeen": NotRequired[datetime],
    },
)
ExploitabilityDetailsTypeDef = TypedDict(
    "ExploitabilityDetailsTypeDef",
    {
        "lastKnownExploitAt": NotRequired[datetime],
    },
)
NumberFilterTypeDef = TypedDict(
    "NumberFilterTypeDef",
    {
        "lowerInclusive": NotRequired[float],
        "upperInclusive": NotRequired[float],
    },
)
PortRangeFilterTypeDef = TypedDict(
    "PortRangeFilterTypeDef",
    {
        "beginInclusive": NotRequired[int],
        "endInclusive": NotRequired[int],
    },
)
FreeTrialInfoTypeDef = TypedDict(
    "FreeTrialInfoTypeDef",
    {
        "end": datetime,
        "start": datetime,
        "status": FreeTrialStatusType,
        "type": FreeTrialTypeType,
    },
)
GetEncryptionKeyRequestRequestTypeDef = TypedDict(
    "GetEncryptionKeyRequestRequestTypeDef",
    {
        "resourceType": ResourceTypeType,
        "scanType": ScanTypeType,
    },
)
GetFindingsReportStatusRequestRequestTypeDef = TypedDict(
    "GetFindingsReportStatusRequestRequestTypeDef",
    {
        "reportId": NotRequired[str],
    },
)
GetMemberRequestRequestTypeDef = TypedDict(
    "GetMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)
MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "accountId": NotRequired[str],
        "delegatedAdminAccountId": NotRequired[str],
        "relationshipStatus": NotRequired[RelationshipStatusType],
        "updatedAt": NotRequired[datetime],
    },
)
GetSbomExportRequestRequestTypeDef = TypedDict(
    "GetSbomExportRequestRequestTypeDef",
    {
        "reportId": str,
    },
)
LambdaFunctionMetadataTypeDef = TypedDict(
    "LambdaFunctionMetadataTypeDef",
    {
        "functionName": NotRequired[str],
        "functionTags": NotRequired[Dict[str, str]],
        "layers": NotRequired[List[str]],
        "runtime": NotRequired[RuntimeType],
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
ListAccountPermissionsRequestRequestTypeDef = TypedDict(
    "ListAccountPermissionsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "service": NotRequired[ServiceType],
    },
)
PermissionTypeDef = TypedDict(
    "PermissionTypeDef",
    {
        "operation": OperationType,
        "service": ServiceType,
    },
)
ListDelegatedAdminAccountsRequestRequestTypeDef = TypedDict(
    "ListDelegatedAdminAccountsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListFiltersRequestRequestTypeDef = TypedDict(
    "ListFiltersRequestRequestTypeDef",
    {
        "action": NotRequired[FilterActionType],
        "arns": NotRequired[Sequence[str]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
SortCriteriaTypeDef = TypedDict(
    "SortCriteriaTypeDef",
    {
        "field": SortFieldType,
        "sortOrder": SortOrderType,
    },
)
ListMembersRequestRequestTypeDef = TypedDict(
    "ListMembersRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "onlyAssociated": NotRequired[bool],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
ListUsageTotalsRequestRequestTypeDef = TypedDict(
    "ListUsageTotalsRequestRequestTypeDef",
    {
        "accountIds": NotRequired[Sequence[str]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
StepTypeDef = TypedDict(
    "StepTypeDef",
    {
        "componentId": str,
        "componentType": str,
    },
)
PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "begin": int,
        "end": int,
    },
)
VulnerablePackageTypeDef = TypedDict(
    "VulnerablePackageTypeDef",
    {
        "name": str,
        "version": str,
        "arch": NotRequired[str],
        "epoch": NotRequired[int],
        "filePath": NotRequired[str],
        "fixedInVersion": NotRequired[str],
        "packageManager": NotRequired[PackageManagerType],
        "release": NotRequired[str],
        "remediation": NotRequired[str],
        "sourceLambdaLayerArn": NotRequired[str],
        "sourceLayerHash": NotRequired[str],
    },
)
RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "Url": NotRequired[str],
        "text": NotRequired[str],
    },
)
ResetEncryptionKeyRequestRequestTypeDef = TypedDict(
    "ResetEncryptionKeyRequestRequestTypeDef",
    {
        "resourceType": ResourceTypeType,
        "scanType": ScanTypeType,
    },
)
ResourceMapFilterTypeDef = TypedDict(
    "ResourceMapFilterTypeDef",
    {
        "comparison": Literal["EQUALS"],
        "key": str,
        "value": NotRequired[str],
    },
)
ResourceStringFilterTypeDef = TypedDict(
    "ResourceStringFilterTypeDef",
    {
        "comparison": ResourceStringComparisonType,
        "value": str,
    },
)
SearchVulnerabilitiesFilterCriteriaTypeDef = TypedDict(
    "SearchVulnerabilitiesFilterCriteriaTypeDef",
    {
        "vulnerabilityIds": Sequence[str],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
UpdateEc2DeepInspectionConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateEc2DeepInspectionConfigurationRequestRequestTypeDef",
    {
        "activateDeepInspection": NotRequired[bool],
        "packagePaths": NotRequired[Sequence[str]],
    },
)
UpdateEncryptionKeyRequestRequestTypeDef = TypedDict(
    "UpdateEncryptionKeyRequestRequestTypeDef",
    {
        "kmsKeyId": str,
        "resourceType": ResourceTypeType,
        "scanType": ScanTypeType,
    },
)
UpdateOrgEc2DeepInspectionConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateOrgEc2DeepInspectionConfigurationRequestRequestTypeDef",
    {
        "orgPackagePaths": Sequence[str],
    },
)
UsageTypeDef = TypedDict(
    "UsageTypeDef",
    {
        "currency": NotRequired[Literal["USD"]],
        "estimatedMonthlyCost": NotRequired[float],
        "total": NotRequired[float],
        "type": NotRequired[UsageTypeType],
    },
)
AccountAggregationResponseTypeDef = TypedDict(
    "AccountAggregationResponseTypeDef",
    {
        "accountId": NotRequired[str],
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
AmiAggregationResponseTypeDef = TypedDict(
    "AmiAggregationResponseTypeDef",
    {
        "ami": str,
        "accountId": NotRequired[str],
        "affectedInstances": NotRequired[int],
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
AwsEcrContainerAggregationResponseTypeDef = TypedDict(
    "AwsEcrContainerAggregationResponseTypeDef",
    {
        "resourceId": str,
        "accountId": NotRequired[str],
        "architecture": NotRequired[str],
        "imageSha": NotRequired[str],
        "imageTags": NotRequired[List[str]],
        "repository": NotRequired[str],
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
Ec2InstanceAggregationResponseTypeDef = TypedDict(
    "Ec2InstanceAggregationResponseTypeDef",
    {
        "instanceId": str,
        "accountId": NotRequired[str],
        "ami": NotRequired[str],
        "instanceTags": NotRequired[Dict[str, str]],
        "networkFindings": NotRequired[int],
        "operatingSystem": NotRequired[str],
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
FindingTypeAggregationResponseTypeDef = TypedDict(
    "FindingTypeAggregationResponseTypeDef",
    {
        "accountId": NotRequired[str],
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
ImageLayerAggregationResponseTypeDef = TypedDict(
    "ImageLayerAggregationResponseTypeDef",
    {
        "accountId": str,
        "layerHash": str,
        "repository": str,
        "resourceId": str,
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
LambdaFunctionAggregationResponseTypeDef = TypedDict(
    "LambdaFunctionAggregationResponseTypeDef",
    {
        "resourceId": str,
        "accountId": NotRequired[str],
        "functionName": NotRequired[str],
        "lambdaTags": NotRequired[Dict[str, str]],
        "lastModifiedAt": NotRequired[datetime],
        "runtime": NotRequired[str],
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
LambdaLayerAggregationResponseTypeDef = TypedDict(
    "LambdaLayerAggregationResponseTypeDef",
    {
        "accountId": str,
        "functionName": str,
        "layerArn": str,
        "resourceId": str,
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
PackageAggregationResponseTypeDef = TypedDict(
    "PackageAggregationResponseTypeDef",
    {
        "packageName": str,
        "accountId": NotRequired[str],
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
RepositoryAggregationResponseTypeDef = TypedDict(
    "RepositoryAggregationResponseTypeDef",
    {
        "repository": str,
        "accountId": NotRequired[str],
        "affectedImages": NotRequired[int],
        "severityCounts": NotRequired[SeverityCountsTypeDef],
    },
)
TitleAggregationResponseTypeDef = TypedDict(
    "TitleAggregationResponseTypeDef",
    {
        "title": str,
        "accountId": NotRequired[str],
        "severityCounts": NotRequired[SeverityCountsTypeDef],
        "vulnerabilityId": NotRequired[str],
    },
)
ResourceStateTypeDef = TypedDict(
    "ResourceStateTypeDef",
    {
        "ec2": StateTypeDef,
        "ecr": StateTypeDef,
        "lambda": NotRequired[StateTypeDef],
        "lambdaCode": NotRequired[StateTypeDef],
    },
)
AccountTypeDef = TypedDict(
    "AccountTypeDef",
    {
        "accountId": str,
        "resourceStatus": ResourceStatusTypeDef,
        "status": StatusType,
    },
)
FailedAccountTypeDef = TypedDict(
    "FailedAccountTypeDef",
    {
        "accountId": str,
        "errorCode": ErrorCodeType,
        "errorMessage": str,
        "resourceStatus": NotRequired[ResourceStatusTypeDef],
        "status": NotRequired[StatusType],
    },
)
AmiAggregationTypeDef = TypedDict(
    "AmiAggregationTypeDef",
    {
        "amis": NotRequired[Sequence[StringFilterTypeDef]],
        "sortBy": NotRequired[AmiSortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
AwsEcrContainerAggregationTypeDef = TypedDict(
    "AwsEcrContainerAggregationTypeDef",
    {
        "architectures": NotRequired[Sequence[StringFilterTypeDef]],
        "imageShas": NotRequired[Sequence[StringFilterTypeDef]],
        "imageTags": NotRequired[Sequence[StringFilterTypeDef]],
        "repositories": NotRequired[Sequence[StringFilterTypeDef]],
        "resourceIds": NotRequired[Sequence[StringFilterTypeDef]],
        "sortBy": NotRequired[AwsEcrContainerSortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
ImageLayerAggregationTypeDef = TypedDict(
    "ImageLayerAggregationTypeDef",
    {
        "layerHashes": NotRequired[Sequence[StringFilterTypeDef]],
        "repositories": NotRequired[Sequence[StringFilterTypeDef]],
        "resourceIds": NotRequired[Sequence[StringFilterTypeDef]],
        "sortBy": NotRequired[ImageLayerSortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
LambdaLayerAggregationTypeDef = TypedDict(
    "LambdaLayerAggregationTypeDef",
    {
        "functionNames": NotRequired[Sequence[StringFilterTypeDef]],
        "layerArns": NotRequired[Sequence[StringFilterTypeDef]],
        "resourceIds": NotRequired[Sequence[StringFilterTypeDef]],
        "sortBy": NotRequired[LambdaLayerSortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
PackageAggregationTypeDef = TypedDict(
    "PackageAggregationTypeDef",
    {
        "packageNames": NotRequired[Sequence[StringFilterTypeDef]],
        "sortBy": NotRequired[PackageSortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
RepositoryAggregationTypeDef = TypedDict(
    "RepositoryAggregationTypeDef",
    {
        "repositories": NotRequired[Sequence[StringFilterTypeDef]],
        "sortBy": NotRequired[RepositorySortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
TitleAggregationTypeDef = TypedDict(
    "TitleAggregationTypeDef",
    {
        "findingType": NotRequired[AggregationFindingTypeType],
        "resourceType": NotRequired[AggregationResourceTypeType],
        "sortBy": NotRequired[TitleSortByType],
        "sortOrder": NotRequired[SortOrderType],
        "titles": NotRequired[Sequence[StringFilterTypeDef]],
        "vulnerabilityIds": NotRequired[Sequence[StringFilterTypeDef]],
    },
)
AssociateMemberResponseTypeDef = TypedDict(
    "AssociateMemberResponseTypeDef",
    {
        "accountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CancelFindingsReportResponseTypeDef = TypedDict(
    "CancelFindingsReportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CancelSbomExportResponseTypeDef = TypedDict(
    "CancelSbomExportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFilterResponseTypeDef = TypedDict(
    "CreateFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFindingsReportResponseTypeDef = TypedDict(
    "CreateFindingsReportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSbomExportResponseTypeDef = TypedDict(
    "CreateSbomExportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteFilterResponseTypeDef = TypedDict(
    "DeleteFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DisableDelegatedAdminAccountResponseTypeDef = TypedDict(
    "DisableDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdminAccountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DisassociateMemberResponseTypeDef = TypedDict(
    "DisassociateMemberResponseTypeDef",
    {
        "accountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnableDelegatedAdminAccountResponseTypeDef = TypedDict(
    "EnableDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdminAccountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetEc2DeepInspectionConfigurationResponseTypeDef = TypedDict(
    "GetEc2DeepInspectionConfigurationResponseTypeDef",
    {
        "errorMessage": str,
        "orgPackagePaths": List[str],
        "packagePaths": List[str],
        "status": Ec2DeepInspectionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetEncryptionKeyResponseTypeDef = TypedDict(
    "GetEncryptionKeyResponseTypeDef",
    {
        "kmsKeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateEc2DeepInspectionConfigurationResponseTypeDef = TypedDict(
    "UpdateEc2DeepInspectionConfigurationResponseTypeDef",
    {
        "errorMessage": str,
        "orgPackagePaths": List[str],
        "packagePaths": List[str],
        "status": Ec2DeepInspectionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFilterResponseTypeDef = TypedDict(
    "UpdateFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeOrganizationConfigurationResponseTypeDef = TypedDict(
    "DescribeOrganizationConfigurationResponseTypeDef",
    {
        "autoEnable": AutoEnableTypeDef,
        "maxAccountLimitReached": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "autoEnable": AutoEnableTypeDef,
    },
)
UpdateOrganizationConfigurationResponseTypeDef = TypedDict(
    "UpdateOrganizationConfigurationResponseTypeDef",
    {
        "autoEnable": AutoEnableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AwsLambdaFunctionDetailsTypeDef = TypedDict(
    "AwsLambdaFunctionDetailsTypeDef",
    {
        "codeSha256": str,
        "executionRoleArn": str,
        "functionName": str,
        "runtime": RuntimeType,
        "version": str,
        "architectures": NotRequired[List[ArchitectureType]],
        "lastModifiedAt": NotRequired[datetime],
        "layers": NotRequired[List[str]],
        "packageType": NotRequired[PackageTypeType],
        "vpcConfig": NotRequired[LambdaVpcConfigTypeDef],
    },
)
BatchGetMemberEc2DeepInspectionStatusResponseTypeDef = TypedDict(
    "BatchGetMemberEc2DeepInspectionStatusResponseTypeDef",
    {
        "accountIds": List[MemberAccountEc2DeepInspectionStatusStateTypeDef],
        "failedAccountIds": List[FailedMemberAccountEc2DeepInspectionStatusStateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchUpdateMemberEc2DeepInspectionStatusResponseTypeDef = TypedDict(
    "BatchUpdateMemberEc2DeepInspectionStatusResponseTypeDef",
    {
        "accountIds": List[MemberAccountEc2DeepInspectionStatusStateTypeDef],
        "failedAccountIds": List[FailedMemberAccountEc2DeepInspectionStatusStateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchUpdateMemberEc2DeepInspectionStatusRequestRequestTypeDef = TypedDict(
    "BatchUpdateMemberEc2DeepInspectionStatusRequestRequestTypeDef",
    {
        "accountIds": Sequence[MemberAccountEc2DeepInspectionStatusTypeDef],
    },
)
CodeVulnerabilityDetailsTypeDef = TypedDict(
    "CodeVulnerabilityDetailsTypeDef",
    {
        "cwes": List[str],
        "detectorId": str,
        "detectorName": str,
        "filePath": CodeFilePathTypeDef,
        "detectorTags": NotRequired[List[str]],
        "referenceUrls": NotRequired[List[str]],
        "ruleId": NotRequired[str],
        "sourceLambdaLayerArn": NotRequired[str],
    },
)
CodeSnippetResultTypeDef = TypedDict(
    "CodeSnippetResultTypeDef",
    {
        "codeSnippet": NotRequired[List[CodeLineTypeDef]],
        "endLine": NotRequired[int],
        "findingArn": NotRequired[str],
        "startLine": NotRequired[int],
        "suggestedFixes": NotRequired[List[SuggestedFixTypeDef]],
    },
)
ListCoverageStatisticsResponseTypeDef = TypedDict(
    "ListCoverageStatisticsResponseTypeDef",
    {
        "countsByGroup": List[CountsTypeDef],
        "nextToken": str,
        "totalCounts": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CoverageDateFilterTypeDef = TypedDict(
    "CoverageDateFilterTypeDef",
    {
        "endInclusive": NotRequired[TimestampTypeDef],
        "startInclusive": NotRequired[TimestampTypeDef],
    },
)
DateFilterTypeDef = TypedDict(
    "DateFilterTypeDef",
    {
        "endInclusive": NotRequired[TimestampTypeDef],
        "startInclusive": NotRequired[TimestampTypeDef],
    },
)
CvssScoreDetailsTypeDef = TypedDict(
    "CvssScoreDetailsTypeDef",
    {
        "score": float,
        "scoreSource": str,
        "scoringVector": str,
        "version": str,
        "adjustments": NotRequired[List[CvssScoreAdjustmentTypeDef]],
        "cvssSource": NotRequired[str],
    },
)
ListDelegatedAdminAccountsResponseTypeDef = TypedDict(
    "ListDelegatedAdminAccountsResponseTypeDef",
    {
        "delegatedAdminAccounts": List[DelegatedAdminAccountTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDelegatedAdminAccountResponseTypeDef = TypedDict(
    "GetDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdmin": DelegatedAdminTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
Ec2InstanceAggregationTypeDef = TypedDict(
    "Ec2InstanceAggregationTypeDef",
    {
        "amis": NotRequired[Sequence[StringFilterTypeDef]],
        "instanceIds": NotRequired[Sequence[StringFilterTypeDef]],
        "instanceTags": NotRequired[Sequence[MapFilterTypeDef]],
        "operatingSystems": NotRequired[Sequence[StringFilterTypeDef]],
        "sortBy": NotRequired[Ec2InstanceSortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
LambdaFunctionAggregationTypeDef = TypedDict(
    "LambdaFunctionAggregationTypeDef",
    {
        "functionNames": NotRequired[Sequence[StringFilterTypeDef]],
        "functionTags": NotRequired[Sequence[MapFilterTypeDef]],
        "resourceIds": NotRequired[Sequence[StringFilterTypeDef]],
        "runtimes": NotRequired[Sequence[StringFilterTypeDef]],
        "sortBy": NotRequired[LambdaFunctionSortByType],
        "sortOrder": NotRequired[SortOrderType],
    },
)
EcrConfigurationStateTypeDef = TypedDict(
    "EcrConfigurationStateTypeDef",
    {
        "rescanDurationState": NotRequired[EcrRescanDurationStateTypeDef],
    },
)
UpdateConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateConfigurationRequestRequestTypeDef",
    {
        "ecrConfiguration": EcrConfigurationTypeDef,
    },
)
FindingDetailTypeDef = TypedDict(
    "FindingDetailTypeDef",
    {
        "cisaData": NotRequired[CisaDataTypeDef],
        "cwes": NotRequired[List[str]],
        "epssScore": NotRequired[float],
        "evidences": NotRequired[List[EvidenceTypeDef]],
        "exploitObserved": NotRequired[ExploitObservedTypeDef],
        "findingArn": NotRequired[str],
        "referenceUrls": NotRequired[List[str]],
        "riskScore": NotRequired[int],
        "tools": NotRequired[List[str]],
        "ttps": NotRequired[List[str]],
    },
)
VulnerabilityTypeDef = TypedDict(
    "VulnerabilityTypeDef",
    {
        "id": str,
        "atigData": NotRequired[AtigDataTypeDef],
        "cisaData": NotRequired[CisaDataTypeDef],
        "cvss2": NotRequired[Cvss2TypeDef],
        "cvss3": NotRequired[Cvss3TypeDef],
        "cwes": NotRequired[List[str]],
        "description": NotRequired[str],
        "detectionPlatforms": NotRequired[List[str]],
        "epss": NotRequired[EpssTypeDef],
        "exploitObserved": NotRequired[ExploitObservedTypeDef],
        "referenceUrls": NotRequired[List[str]],
        "relatedVulnerabilities": NotRequired[List[str]],
        "source": NotRequired[Literal["NVD"]],
        "sourceUrl": NotRequired[str],
        "vendorCreatedAt": NotRequired[datetime],
        "vendorSeverity": NotRequired[str],
        "vendorUpdatedAt": NotRequired[datetime],
    },
)
PackageFilterTypeDef = TypedDict(
    "PackageFilterTypeDef",
    {
        "architecture": NotRequired[StringFilterTypeDef],
        "epoch": NotRequired[NumberFilterTypeDef],
        "name": NotRequired[StringFilterTypeDef],
        "release": NotRequired[StringFilterTypeDef],
        "sourceLambdaLayerArn": NotRequired[StringFilterTypeDef],
        "sourceLayerHash": NotRequired[StringFilterTypeDef],
        "version": NotRequired[StringFilterTypeDef],
    },
)
FreeTrialAccountInfoTypeDef = TypedDict(
    "FreeTrialAccountInfoTypeDef",
    {
        "accountId": str,
        "freeTrialInfo": List[FreeTrialInfoTypeDef],
    },
)
GetMemberResponseTypeDef = TypedDict(
    "GetMemberResponseTypeDef",
    {
        "member": MemberTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListMembersResponseTypeDef = TypedDict(
    "ListMembersResponseTypeDef",
    {
        "members": List[MemberTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResourceScanMetadataTypeDef = TypedDict(
    "ResourceScanMetadataTypeDef",
    {
        "ec2": NotRequired[Ec2MetadataTypeDef],
        "ecrImage": NotRequired[EcrContainerImageMetadataTypeDef],
        "ecrRepository": NotRequired[EcrRepositoryMetadataTypeDef],
        "lambdaFunction": NotRequired[LambdaFunctionMetadataTypeDef],
    },
)
ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef = TypedDict(
    "ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef",
    {
        "service": NotRequired[ServiceType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef = TypedDict(
    "ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFiltersRequestListFiltersPaginateTypeDef = TypedDict(
    "ListFiltersRequestListFiltersPaginateTypeDef",
    {
        "action": NotRequired[FilterActionType],
        "arns": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListMembersRequestListMembersPaginateTypeDef = TypedDict(
    "ListMembersRequestListMembersPaginateTypeDef",
    {
        "onlyAssociated": NotRequired[bool],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListUsageTotalsRequestListUsageTotalsPaginateTypeDef = TypedDict(
    "ListUsageTotalsRequestListUsageTotalsPaginateTypeDef",
    {
        "accountIds": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAccountPermissionsResponseTypeDef = TypedDict(
    "ListAccountPermissionsResponseTypeDef",
    {
        "nextToken": str,
        "permissions": List[PermissionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
NetworkPathTypeDef = TypedDict(
    "NetworkPathTypeDef",
    {
        "steps": NotRequired[List[StepTypeDef]],
    },
)
PackageVulnerabilityDetailsTypeDef = TypedDict(
    "PackageVulnerabilityDetailsTypeDef",
    {
        "source": str,
        "vulnerabilityId": str,
        "cvss": NotRequired[List[CvssScoreTypeDef]],
        "referenceUrls": NotRequired[List[str]],
        "relatedVulnerabilities": NotRequired[List[str]],
        "sourceUrl": NotRequired[str],
        "vendorCreatedAt": NotRequired[datetime],
        "vendorSeverity": NotRequired[str],
        "vendorUpdatedAt": NotRequired[datetime],
        "vulnerablePackages": NotRequired[List[VulnerablePackageTypeDef]],
    },
)
RemediationTypeDef = TypedDict(
    "RemediationTypeDef",
    {
        "recommendation": NotRequired[RecommendationTypeDef],
    },
)
ResourceFilterCriteriaTypeDef = TypedDict(
    "ResourceFilterCriteriaTypeDef",
    {
        "accountId": NotRequired[Sequence[ResourceStringFilterTypeDef]],
        "ec2InstanceTags": NotRequired[Sequence[ResourceMapFilterTypeDef]],
        "ecrImageTags": NotRequired[Sequence[ResourceStringFilterTypeDef]],
        "ecrRepositoryName": NotRequired[Sequence[ResourceStringFilterTypeDef]],
        "lambdaFunctionName": NotRequired[Sequence[ResourceStringFilterTypeDef]],
        "lambdaFunctionTags": NotRequired[Sequence[ResourceMapFilterTypeDef]],
        "resourceId": NotRequired[Sequence[ResourceStringFilterTypeDef]],
        "resourceType": NotRequired[Sequence[ResourceStringFilterTypeDef]],
    },
)
SearchVulnerabilitiesRequestRequestTypeDef = TypedDict(
    "SearchVulnerabilitiesRequestRequestTypeDef",
    {
        "filterCriteria": SearchVulnerabilitiesFilterCriteriaTypeDef,
        "nextToken": NotRequired[str],
    },
)
SearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef = TypedDict(
    "SearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef",
    {
        "filterCriteria": SearchVulnerabilitiesFilterCriteriaTypeDef,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
UsageTotalTypeDef = TypedDict(
    "UsageTotalTypeDef",
    {
        "accountId": NotRequired[str],
        "usage": NotRequired[List[UsageTypeDef]],
    },
)
AggregationResponseTypeDef = TypedDict(
    "AggregationResponseTypeDef",
    {
        "accountAggregation": NotRequired[AccountAggregationResponseTypeDef],
        "amiAggregation": NotRequired[AmiAggregationResponseTypeDef],
        "awsEcrContainerAggregation": NotRequired[AwsEcrContainerAggregationResponseTypeDef],
        "ec2InstanceAggregation": NotRequired[Ec2InstanceAggregationResponseTypeDef],
        "findingTypeAggregation": NotRequired[FindingTypeAggregationResponseTypeDef],
        "imageLayerAggregation": NotRequired[ImageLayerAggregationResponseTypeDef],
        "lambdaFunctionAggregation": NotRequired[LambdaFunctionAggregationResponseTypeDef],
        "lambdaLayerAggregation": NotRequired[LambdaLayerAggregationResponseTypeDef],
        "packageAggregation": NotRequired[PackageAggregationResponseTypeDef],
        "repositoryAggregation": NotRequired[RepositoryAggregationResponseTypeDef],
        "titleAggregation": NotRequired[TitleAggregationResponseTypeDef],
    },
)
AccountStateTypeDef = TypedDict(
    "AccountStateTypeDef",
    {
        "accountId": str,
        "resourceState": ResourceStateTypeDef,
        "state": StateTypeDef,
    },
)
DisableResponseTypeDef = TypedDict(
    "DisableResponseTypeDef",
    {
        "accounts": List[AccountTypeDef],
        "failedAccounts": List[FailedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnableResponseTypeDef = TypedDict(
    "EnableResponseTypeDef",
    {
        "accounts": List[AccountTypeDef],
        "failedAccounts": List[FailedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "awsEc2Instance": NotRequired[AwsEc2InstanceDetailsTypeDef],
        "awsEcrContainerImage": NotRequired[AwsEcrContainerImageDetailsTypeDef],
        "awsLambdaFunction": NotRequired[AwsLambdaFunctionDetailsTypeDef],
    },
)
BatchGetCodeSnippetResponseTypeDef = TypedDict(
    "BatchGetCodeSnippetResponseTypeDef",
    {
        "codeSnippetResults": List[CodeSnippetResultTypeDef],
        "errors": List[CodeSnippetErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CoverageFilterCriteriaTypeDef = TypedDict(
    "CoverageFilterCriteriaTypeDef",
    {
        "accountId": NotRequired[Sequence[CoverageStringFilterTypeDef]],
        "ec2InstanceTags": NotRequired[Sequence[CoverageMapFilterTypeDef]],
        "ecrImageTags": NotRequired[Sequence[CoverageStringFilterTypeDef]],
        "ecrRepositoryName": NotRequired[Sequence[CoverageStringFilterTypeDef]],
        "lambdaFunctionName": NotRequired[Sequence[CoverageStringFilterTypeDef]],
        "lambdaFunctionRuntime": NotRequired[Sequence[CoverageStringFilterTypeDef]],
        "lambdaFunctionTags": NotRequired[Sequence[CoverageMapFilterTypeDef]],
        "lastScannedAt": NotRequired[Sequence[CoverageDateFilterTypeDef]],
        "resourceId": NotRequired[Sequence[CoverageStringFilterTypeDef]],
        "resourceType": NotRequired[Sequence[CoverageStringFilterTypeDef]],
        "scanStatusCode": NotRequired[Sequence[CoverageStringFilterTypeDef]],
        "scanStatusReason": NotRequired[Sequence[CoverageStringFilterTypeDef]],
        "scanType": NotRequired[Sequence[CoverageStringFilterTypeDef]],
    },
)
InspectorScoreDetailsTypeDef = TypedDict(
    "InspectorScoreDetailsTypeDef",
    {
        "adjustedCvss": NotRequired[CvssScoreDetailsTypeDef],
    },
)
AggregationRequestTypeDef = TypedDict(
    "AggregationRequestTypeDef",
    {
        "accountAggregation": NotRequired[AccountAggregationTypeDef],
        "amiAggregation": NotRequired[AmiAggregationTypeDef],
        "awsEcrContainerAggregation": NotRequired[AwsEcrContainerAggregationTypeDef],
        "ec2InstanceAggregation": NotRequired[Ec2InstanceAggregationTypeDef],
        "findingTypeAggregation": NotRequired[FindingTypeAggregationTypeDef],
        "imageLayerAggregation": NotRequired[ImageLayerAggregationTypeDef],
        "lambdaFunctionAggregation": NotRequired[LambdaFunctionAggregationTypeDef],
        "lambdaLayerAggregation": NotRequired[LambdaLayerAggregationTypeDef],
        "packageAggregation": NotRequired[PackageAggregationTypeDef],
        "repositoryAggregation": NotRequired[RepositoryAggregationTypeDef],
        "titleAggregation": NotRequired[TitleAggregationTypeDef],
    },
)
GetConfigurationResponseTypeDef = TypedDict(
    "GetConfigurationResponseTypeDef",
    {
        "ecrConfiguration": EcrConfigurationStateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchGetFindingDetailsResponseTypeDef = TypedDict(
    "BatchGetFindingDetailsResponseTypeDef",
    {
        "errors": List[FindingDetailsErrorTypeDef],
        "findingDetails": List[FindingDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SearchVulnerabilitiesResponseTypeDef = TypedDict(
    "SearchVulnerabilitiesResponseTypeDef",
    {
        "nextToken": str,
        "vulnerabilities": List[VulnerabilityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FilterCriteriaPaginatorTypeDef = TypedDict(
    "FilterCriteriaPaginatorTypeDef",
    {
        "awsAccountId": NotRequired[List[StringFilterTypeDef]],
        "codeVulnerabilityDetectorName": NotRequired[List[StringFilterTypeDef]],
        "codeVulnerabilityDetectorTags": NotRequired[List[StringFilterTypeDef]],
        "codeVulnerabilityFilePath": NotRequired[List[StringFilterTypeDef]],
        "componentId": NotRequired[List[StringFilterTypeDef]],
        "componentType": NotRequired[List[StringFilterTypeDef]],
        "ec2InstanceImageId": NotRequired[List[StringFilterTypeDef]],
        "ec2InstanceSubnetId": NotRequired[List[StringFilterTypeDef]],
        "ec2InstanceVpcId": NotRequired[List[StringFilterTypeDef]],
        "ecrImageArchitecture": NotRequired[List[StringFilterTypeDef]],
        "ecrImageHash": NotRequired[List[StringFilterTypeDef]],
        "ecrImagePushedAt": NotRequired[List[DateFilterPaginatorTypeDef]],
        "ecrImageRegistry": NotRequired[List[StringFilterTypeDef]],
        "ecrImageRepositoryName": NotRequired[List[StringFilterTypeDef]],
        "ecrImageTags": NotRequired[List[StringFilterTypeDef]],
        "epssScore": NotRequired[List[NumberFilterTypeDef]],
        "exploitAvailable": NotRequired[List[StringFilterTypeDef]],
        "findingArn": NotRequired[List[StringFilterTypeDef]],
        "findingStatus": NotRequired[List[StringFilterTypeDef]],
        "findingType": NotRequired[List[StringFilterTypeDef]],
        "firstObservedAt": NotRequired[List[DateFilterPaginatorTypeDef]],
        "fixAvailable": NotRequired[List[StringFilterTypeDef]],
        "inspectorScore": NotRequired[List[NumberFilterTypeDef]],
        "lambdaFunctionExecutionRoleArn": NotRequired[List[StringFilterTypeDef]],
        "lambdaFunctionLastModifiedAt": NotRequired[List[DateFilterPaginatorTypeDef]],
        "lambdaFunctionLayers": NotRequired[List[StringFilterTypeDef]],
        "lambdaFunctionName": NotRequired[List[StringFilterTypeDef]],
        "lambdaFunctionRuntime": NotRequired[List[StringFilterTypeDef]],
        "lastObservedAt": NotRequired[List[DateFilterPaginatorTypeDef]],
        "networkProtocol": NotRequired[List[StringFilterTypeDef]],
        "portRange": NotRequired[List[PortRangeFilterTypeDef]],
        "relatedVulnerabilities": NotRequired[List[StringFilterTypeDef]],
        "resourceId": NotRequired[List[StringFilterTypeDef]],
        "resourceTags": NotRequired[List[MapFilterTypeDef]],
        "resourceType": NotRequired[List[StringFilterTypeDef]],
        "severity": NotRequired[List[StringFilterTypeDef]],
        "title": NotRequired[List[StringFilterTypeDef]],
        "updatedAt": NotRequired[List[DateFilterPaginatorTypeDef]],
        "vendorSeverity": NotRequired[List[StringFilterTypeDef]],
        "vulnerabilityId": NotRequired[List[StringFilterTypeDef]],
        "vulnerabilitySource": NotRequired[List[StringFilterTypeDef]],
        "vulnerablePackages": NotRequired[List[PackageFilterTypeDef]],
    },
)
FilterCriteriaTypeDef = TypedDict(
    "FilterCriteriaTypeDef",
    {
        "awsAccountId": NotRequired[Sequence[StringFilterTypeDef]],
        "codeVulnerabilityDetectorName": NotRequired[Sequence[StringFilterTypeDef]],
        "codeVulnerabilityDetectorTags": NotRequired[Sequence[StringFilterTypeDef]],
        "codeVulnerabilityFilePath": NotRequired[Sequence[StringFilterTypeDef]],
        "componentId": NotRequired[Sequence[StringFilterTypeDef]],
        "componentType": NotRequired[Sequence[StringFilterTypeDef]],
        "ec2InstanceImageId": NotRequired[Sequence[StringFilterTypeDef]],
        "ec2InstanceSubnetId": NotRequired[Sequence[StringFilterTypeDef]],
        "ec2InstanceVpcId": NotRequired[Sequence[StringFilterTypeDef]],
        "ecrImageArchitecture": NotRequired[Sequence[StringFilterTypeDef]],
        "ecrImageHash": NotRequired[Sequence[StringFilterTypeDef]],
        "ecrImagePushedAt": NotRequired[Sequence[DateFilterTypeDef]],
        "ecrImageRegistry": NotRequired[Sequence[StringFilterTypeDef]],
        "ecrImageRepositoryName": NotRequired[Sequence[StringFilterTypeDef]],
        "ecrImageTags": NotRequired[Sequence[StringFilterTypeDef]],
        "epssScore": NotRequired[Sequence[NumberFilterTypeDef]],
        "exploitAvailable": NotRequired[Sequence[StringFilterTypeDef]],
        "findingArn": NotRequired[Sequence[StringFilterTypeDef]],
        "findingStatus": NotRequired[Sequence[StringFilterTypeDef]],
        "findingType": NotRequired[Sequence[StringFilterTypeDef]],
        "firstObservedAt": NotRequired[Sequence[DateFilterTypeDef]],
        "fixAvailable": NotRequired[Sequence[StringFilterTypeDef]],
        "inspectorScore": NotRequired[Sequence[NumberFilterTypeDef]],
        "lambdaFunctionExecutionRoleArn": NotRequired[Sequence[StringFilterTypeDef]],
        "lambdaFunctionLastModifiedAt": NotRequired[Sequence[DateFilterTypeDef]],
        "lambdaFunctionLayers": NotRequired[Sequence[StringFilterTypeDef]],
        "lambdaFunctionName": NotRequired[Sequence[StringFilterTypeDef]],
        "lambdaFunctionRuntime": NotRequired[Sequence[StringFilterTypeDef]],
        "lastObservedAt": NotRequired[Sequence[DateFilterTypeDef]],
        "networkProtocol": NotRequired[Sequence[StringFilterTypeDef]],
        "portRange": NotRequired[Sequence[PortRangeFilterTypeDef]],
        "relatedVulnerabilities": NotRequired[Sequence[StringFilterTypeDef]],
        "resourceId": NotRequired[Sequence[StringFilterTypeDef]],
        "resourceTags": NotRequired[Sequence[MapFilterTypeDef]],
        "resourceType": NotRequired[Sequence[StringFilterTypeDef]],
        "severity": NotRequired[Sequence[StringFilterTypeDef]],
        "title": NotRequired[Sequence[StringFilterTypeDef]],
        "updatedAt": NotRequired[Sequence[DateFilterTypeDef]],
        "vendorSeverity": NotRequired[Sequence[StringFilterTypeDef]],
        "vulnerabilityId": NotRequired[Sequence[StringFilterTypeDef]],
        "vulnerabilitySource": NotRequired[Sequence[StringFilterTypeDef]],
        "vulnerablePackages": NotRequired[Sequence[PackageFilterTypeDef]],
    },
)
BatchGetFreeTrialInfoResponseTypeDef = TypedDict(
    "BatchGetFreeTrialInfoResponseTypeDef",
    {
        "accounts": List[FreeTrialAccountInfoTypeDef],
        "failedAccounts": List[FreeTrialInfoErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CoveredResourceTypeDef = TypedDict(
    "CoveredResourceTypeDef",
    {
        "accountId": str,
        "resourceId": str,
        "resourceType": CoverageResourceTypeType,
        "scanType": ScanTypeType,
        "lastScannedAt": NotRequired[datetime],
        "resourceMetadata": NotRequired[ResourceScanMetadataTypeDef],
        "scanStatus": NotRequired[ScanStatusTypeDef],
    },
)
NetworkReachabilityDetailsTypeDef = TypedDict(
    "NetworkReachabilityDetailsTypeDef",
    {
        "networkPath": NetworkPathTypeDef,
        "openPortRange": PortRangeTypeDef,
        "protocol": NetworkProtocolType,
    },
)
CreateSbomExportRequestRequestTypeDef = TypedDict(
    "CreateSbomExportRequestRequestTypeDef",
    {
        "reportFormat": SbomReportFormatType,
        "s3Destination": DestinationTypeDef,
        "resourceFilterCriteria": NotRequired[ResourceFilterCriteriaTypeDef],
    },
)
GetSbomExportResponseTypeDef = TypedDict(
    "GetSbomExportResponseTypeDef",
    {
        "errorCode": ReportingErrorCodeType,
        "errorMessage": str,
        "filterCriteria": ResourceFilterCriteriaTypeDef,
        "format": SbomReportFormatType,
        "reportId": str,
        "s3Destination": DestinationTypeDef,
        "status": ExternalReportStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListUsageTotalsResponseTypeDef = TypedDict(
    "ListUsageTotalsResponseTypeDef",
    {
        "nextToken": str,
        "totals": List[UsageTotalTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFindingAggregationsResponseTypeDef = TypedDict(
    "ListFindingAggregationsResponseTypeDef",
    {
        "aggregationType": AggregationTypeType,
        "nextToken": str,
        "responses": List[AggregationResponseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchGetAccountStatusResponseTypeDef = TypedDict(
    "BatchGetAccountStatusResponseTypeDef",
    {
        "accounts": List[AccountStateTypeDef],
        "failedAccounts": List[FailedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "id": str,
        "type": ResourceTypeType,
        "details": NotRequired[ResourceDetailsTypeDef],
        "partition": NotRequired[str],
        "region": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
ListCoverageRequestListCoveragePaginateTypeDef = TypedDict(
    "ListCoverageRequestListCoveragePaginateTypeDef",
    {
        "filterCriteria": NotRequired[CoverageFilterCriteriaTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListCoverageRequestRequestTypeDef = TypedDict(
    "ListCoverageRequestRequestTypeDef",
    {
        "filterCriteria": NotRequired[CoverageFilterCriteriaTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef = TypedDict(
    "ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef",
    {
        "filterCriteria": NotRequired[CoverageFilterCriteriaTypeDef],
        "groupBy": NotRequired[GroupKeyType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListCoverageStatisticsRequestRequestTypeDef = TypedDict(
    "ListCoverageStatisticsRequestRequestTypeDef",
    {
        "filterCriteria": NotRequired[CoverageFilterCriteriaTypeDef],
        "groupBy": NotRequired[GroupKeyType],
        "nextToken": NotRequired[str],
    },
)
ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef = TypedDict(
    "ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    {
        "aggregationType": AggregationTypeType,
        "accountIds": NotRequired[Sequence[StringFilterTypeDef]],
        "aggregationRequest": NotRequired[AggregationRequestTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFindingAggregationsRequestRequestTypeDef = TypedDict(
    "ListFindingAggregationsRequestRequestTypeDef",
    {
        "aggregationType": AggregationTypeType,
        "accountIds": NotRequired[Sequence[StringFilterTypeDef]],
        "aggregationRequest": NotRequired[AggregationRequestTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
FilterPaginatorTypeDef = TypedDict(
    "FilterPaginatorTypeDef",
    {
        "action": FilterActionType,
        "arn": str,
        "createdAt": datetime,
        "criteria": FilterCriteriaPaginatorTypeDef,
        "name": str,
        "ownerId": str,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "reason": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
ListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "ListFindingsRequestListFindingsPaginateTypeDef",
    {
        "filterCriteria": NotRequired[FilterCriteriaPaginatorTypeDef],
        "sortCriteria": NotRequired[SortCriteriaTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
CreateFilterRequestRequestTypeDef = TypedDict(
    "CreateFilterRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "filterCriteria": FilterCriteriaTypeDef,
        "name": str,
        "description": NotRequired[str],
        "reason": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateFindingsReportRequestRequestTypeDef = TypedDict(
    "CreateFindingsReportRequestRequestTypeDef",
    {
        "reportFormat": ReportFormatType,
        "s3Destination": DestinationTypeDef,
        "filterCriteria": NotRequired[FilterCriteriaTypeDef],
    },
)
FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "action": FilterActionType,
        "arn": str,
        "createdAt": datetime,
        "criteria": FilterCriteriaTypeDef,
        "name": str,
        "ownerId": str,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "reason": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
GetFindingsReportStatusResponseTypeDef = TypedDict(
    "GetFindingsReportStatusResponseTypeDef",
    {
        "destination": DestinationTypeDef,
        "errorCode": ReportingErrorCodeType,
        "errorMessage": str,
        "filterCriteria": FilterCriteriaTypeDef,
        "reportId": str,
        "status": ExternalReportStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFindingsRequestRequestTypeDef = TypedDict(
    "ListFindingsRequestRequestTypeDef",
    {
        "filterCriteria": NotRequired[FilterCriteriaTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "sortCriteria": NotRequired[SortCriteriaTypeDef],
    },
)
UpdateFilterRequestRequestTypeDef = TypedDict(
    "UpdateFilterRequestRequestTypeDef",
    {
        "filterArn": str,
        "action": NotRequired[FilterActionType],
        "description": NotRequired[str],
        "filterCriteria": NotRequired[FilterCriteriaTypeDef],
        "name": NotRequired[str],
        "reason": NotRequired[str],
    },
)
ListCoverageResponseTypeDef = TypedDict(
    "ListCoverageResponseTypeDef",
    {
        "coveredResources": List[CoveredResourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FindingTypeDef = TypedDict(
    "FindingTypeDef",
    {
        "awsAccountId": str,
        "description": str,
        "findingArn": str,
        "firstObservedAt": datetime,
        "lastObservedAt": datetime,
        "remediation": RemediationTypeDef,
        "resources": List[ResourceTypeDef],
        "severity": SeverityType,
        "status": FindingStatusType,
        "type": FindingTypeType,
        "codeVulnerabilityDetails": NotRequired[CodeVulnerabilityDetailsTypeDef],
        "epss": NotRequired[EpssDetailsTypeDef],
        "exploitAvailable": NotRequired[ExploitAvailableType],
        "exploitabilityDetails": NotRequired[ExploitabilityDetailsTypeDef],
        "fixAvailable": NotRequired[FixAvailableType],
        "inspectorScore": NotRequired[float],
        "inspectorScoreDetails": NotRequired[InspectorScoreDetailsTypeDef],
        "networkReachabilityDetails": NotRequired[NetworkReachabilityDetailsTypeDef],
        "packageVulnerabilityDetails": NotRequired[PackageVulnerabilityDetailsTypeDef],
        "title": NotRequired[str],
        "updatedAt": NotRequired[datetime],
    },
)
ListFiltersResponsePaginatorTypeDef = TypedDict(
    "ListFiltersResponsePaginatorTypeDef",
    {
        "filters": List[FilterPaginatorTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFiltersResponseTypeDef = TypedDict(
    "ListFiltersResponseTypeDef",
    {
        "filters": List[FilterTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFindingsResponseTypeDef = TypedDict(
    "ListFindingsResponseTypeDef",
    {
        "findings": List[FindingTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
