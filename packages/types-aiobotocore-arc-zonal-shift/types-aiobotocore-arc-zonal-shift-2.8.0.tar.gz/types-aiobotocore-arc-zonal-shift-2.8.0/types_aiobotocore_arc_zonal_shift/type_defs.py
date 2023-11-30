"""
Type annotations for arc-zonal-shift service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/type_defs/)

Usage::

    ```python
    from types_aiobotocore_arc_zonal_shift.type_defs import CancelZonalShiftRequestRequestTypeDef

    data: CancelZonalShiftRequestRequestTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List

from .literals import AppliedStatusType, ZonalShiftStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CancelZonalShiftRequestRequestTypeDef",
    "GetManagedResourceRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ZonalShiftInResourceTypeDef",
    "PaginatorConfigTypeDef",
    "ListManagedResourcesRequestRequestTypeDef",
    "ManagedResourceSummaryTypeDef",
    "ListZonalShiftsRequestRequestTypeDef",
    "ZonalShiftSummaryTypeDef",
    "StartZonalShiftRequestRequestTypeDef",
    "UpdateZonalShiftRequestRequestTypeDef",
    "ZonalShiftTypeDef",
    "GetManagedResourceResponseTypeDef",
    "ListManagedResourcesRequestListManagedResourcesPaginateTypeDef",
    "ListZonalShiftsRequestListZonalShiftsPaginateTypeDef",
    "ListManagedResourcesResponseTypeDef",
    "ListZonalShiftsResponseTypeDef",
)

CancelZonalShiftRequestRequestTypeDef = TypedDict(
    "CancelZonalShiftRequestRequestTypeDef",
    {
        "zonalShiftId": str,
    },
)
GetManagedResourceRequestRequestTypeDef = TypedDict(
    "GetManagedResourceRequestRequestTypeDef",
    {
        "resourceIdentifier": str,
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
ZonalShiftInResourceTypeDef = TypedDict(
    "ZonalShiftInResourceTypeDef",
    {
        "appliedStatus": AppliedStatusType,
        "awayFrom": str,
        "comment": str,
        "expiryTime": datetime,
        "resourceIdentifier": str,
        "startTime": datetime,
        "zonalShiftId": str,
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
ListManagedResourcesRequestRequestTypeDef = TypedDict(
    "ListManagedResourcesRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ManagedResourceSummaryTypeDef = TypedDict(
    "ManagedResourceSummaryTypeDef",
    {
        "availabilityZones": List[str],
        "arn": NotRequired[str],
        "name": NotRequired[str],
    },
)
ListZonalShiftsRequestRequestTypeDef = TypedDict(
    "ListZonalShiftsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "status": NotRequired[ZonalShiftStatusType],
    },
)
ZonalShiftSummaryTypeDef = TypedDict(
    "ZonalShiftSummaryTypeDef",
    {
        "awayFrom": str,
        "comment": str,
        "expiryTime": datetime,
        "resourceIdentifier": str,
        "startTime": datetime,
        "status": ZonalShiftStatusType,
        "zonalShiftId": str,
    },
)
StartZonalShiftRequestRequestTypeDef = TypedDict(
    "StartZonalShiftRequestRequestTypeDef",
    {
        "awayFrom": str,
        "comment": str,
        "expiresIn": str,
        "resourceIdentifier": str,
    },
)
UpdateZonalShiftRequestRequestTypeDef = TypedDict(
    "UpdateZonalShiftRequestRequestTypeDef",
    {
        "zonalShiftId": str,
        "comment": NotRequired[str],
        "expiresIn": NotRequired[str],
    },
)
ZonalShiftTypeDef = TypedDict(
    "ZonalShiftTypeDef",
    {
        "awayFrom": str,
        "comment": str,
        "expiryTime": datetime,
        "resourceIdentifier": str,
        "startTime": datetime,
        "status": ZonalShiftStatusType,
        "zonalShiftId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetManagedResourceResponseTypeDef = TypedDict(
    "GetManagedResourceResponseTypeDef",
    {
        "appliedWeights": Dict[str, float],
        "arn": str,
        "name": str,
        "zonalShifts": List[ZonalShiftInResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListManagedResourcesRequestListManagedResourcesPaginateTypeDef = TypedDict(
    "ListManagedResourcesRequestListManagedResourcesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListZonalShiftsRequestListZonalShiftsPaginateTypeDef = TypedDict(
    "ListZonalShiftsRequestListZonalShiftsPaginateTypeDef",
    {
        "status": NotRequired[ZonalShiftStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListManagedResourcesResponseTypeDef = TypedDict(
    "ListManagedResourcesResponseTypeDef",
    {
        "items": List[ManagedResourceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListZonalShiftsResponseTypeDef = TypedDict(
    "ListZonalShiftsResponseTypeDef",
    {
        "items": List[ZonalShiftSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
