"""
Type annotations for ssm-contacts service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ssm_contacts.client import SSMContactsClient
    from mypy_boto3_ssm_contacts.paginator import (
        ListContactChannelsPaginator,
        ListContactsPaginator,
        ListEngagementsPaginator,
        ListPageReceiptsPaginator,
        ListPageResolutionsPaginator,
        ListPagesByContactPaginator,
        ListPagesByEngagementPaginator,
        ListPreviewRotationShiftsPaginator,
        ListRotationOverridesPaginator,
        ListRotationShiftsPaginator,
        ListRotationsPaginator,
    )

    session = Session()
    client: SSMContactsClient = session.client("ssm-contacts")

    list_contact_channels_paginator: ListContactChannelsPaginator = client.get_paginator("list_contact_channels")
    list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
    list_engagements_paginator: ListEngagementsPaginator = client.get_paginator("list_engagements")
    list_page_receipts_paginator: ListPageReceiptsPaginator = client.get_paginator("list_page_receipts")
    list_page_resolutions_paginator: ListPageResolutionsPaginator = client.get_paginator("list_page_resolutions")
    list_pages_by_contact_paginator: ListPagesByContactPaginator = client.get_paginator("list_pages_by_contact")
    list_pages_by_engagement_paginator: ListPagesByEngagementPaginator = client.get_paginator("list_pages_by_engagement")
    list_preview_rotation_shifts_paginator: ListPreviewRotationShiftsPaginator = client.get_paginator("list_preview_rotation_shifts")
    list_rotation_overrides_paginator: ListRotationOverridesPaginator = client.get_paginator("list_rotation_overrides")
    list_rotation_shifts_paginator: ListRotationShiftsPaginator = client.get_paginator("list_rotation_shifts")
    list_rotations_paginator: ListRotationsPaginator = client.get_paginator("list_rotations")
    ```
"""

from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import ContactTypeType
from .type_defs import (
    ListContactChannelsResultTypeDef,
    ListContactsResultTypeDef,
    ListEngagementsResultTypeDef,
    ListPageReceiptsResultTypeDef,
    ListPageResolutionsResultTypeDef,
    ListPagesByContactResultTypeDef,
    ListPagesByEngagementResultTypeDef,
    ListPreviewRotationShiftsResultTypeDef,
    ListRotationOverridesResultTypeDef,
    ListRotationShiftsResultTypeDef,
    ListRotationsResultTypeDef,
    PaginatorConfigTypeDef,
    PreviewOverrideTypeDef,
    RecurrenceSettingsTypeDef,
    TimeRangeTypeDef,
    TimestampTypeDef,
)

__all__ = (
    "ListContactChannelsPaginator",
    "ListContactsPaginator",
    "ListEngagementsPaginator",
    "ListPageReceiptsPaginator",
    "ListPageResolutionsPaginator",
    "ListPagesByContactPaginator",
    "ListPagesByEngagementPaginator",
    "ListPreviewRotationShiftsPaginator",
    "ListRotationOverridesPaginator",
    "ListRotationShiftsPaginator",
    "ListRotationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListContactChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContactChannels)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listcontactchannelspaginator)
    """

    def paginate(
        self, *, ContactId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContactChannelsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContactChannels.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listcontactchannelspaginator)
        """


class ListContactsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContacts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listcontactspaginator)
    """

    def paginate(
        self,
        *,
        AliasPrefix: str = ...,
        Type: ContactTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContacts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listcontactspaginator)
        """


class ListEngagementsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListEngagements)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listengagementspaginator)
    """

    def paginate(
        self,
        *,
        IncidentId: str = ...,
        TimeRangeValue: TimeRangeTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEngagementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListEngagements.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listengagementspaginator)
        """


class ListPageReceiptsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPageReceipts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagereceiptspaginator)
    """

    def paginate(
        self, *, PageId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPageReceiptsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPageReceipts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagereceiptspaginator)
        """


class ListPageResolutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPageResolutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpageresolutionspaginator)
    """

    def paginate(
        self, *, PageId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPageResolutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPageResolutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpageresolutionspaginator)
        """


class ListPagesByContactPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByContact)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagesbycontactpaginator)
    """

    def paginate(
        self, *, ContactId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPagesByContactResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByContact.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagesbycontactpaginator)
        """


class ListPagesByEngagementPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByEngagement)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagesbyengagementpaginator)
    """

    def paginate(
        self, *, EngagementId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPagesByEngagementResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByEngagement.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpagesbyengagementpaginator)
        """


class ListPreviewRotationShiftsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPreviewRotationShifts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpreviewrotationshiftspaginator)
    """

    def paginate(
        self,
        *,
        EndTime: TimestampTypeDef,
        Members: Sequence[str],
        TimeZoneId: str,
        Recurrence: RecurrenceSettingsTypeDef,
        RotationStartTime: TimestampTypeDef = ...,
        StartTime: TimestampTypeDef = ...,
        Overrides: Sequence[PreviewOverrideTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPreviewRotationShiftsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPreviewRotationShifts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listpreviewrotationshiftspaginator)
        """


class ListRotationOverridesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListRotationOverrides)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listrotationoverridespaginator)
    """

    def paginate(
        self,
        *,
        RotationId: str,
        StartTime: TimestampTypeDef,
        EndTime: TimestampTypeDef,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRotationOverridesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListRotationOverrides.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listrotationoverridespaginator)
        """


class ListRotationShiftsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListRotationShifts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listrotationshiftspaginator)
    """

    def paginate(
        self,
        *,
        RotationId: str,
        EndTime: TimestampTypeDef,
        StartTime: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRotationShiftsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListRotationShifts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listrotationshiftspaginator)
        """


class ListRotationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListRotations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listrotationspaginator)
    """

    def paginate(
        self, *, RotationNamePrefix: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRotationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListRotations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/paginators/#listrotationspaginator)
        """
