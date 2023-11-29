"""
Type annotations for scheduler service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_scheduler.client import EventBridgeSchedulerClient
    from mypy_boto3_scheduler.paginator import (
        ListScheduleGroupsPaginator,
        ListSchedulesPaginator,
    )

    session = Session()
    client: EventBridgeSchedulerClient = session.client("scheduler")

    list_schedule_groups_paginator: ListScheduleGroupsPaginator = client.get_paginator("list_schedule_groups")
    list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import ScheduleStateType
from .type_defs import (
    ListScheduleGroupsOutputTypeDef,
    ListSchedulesOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListScheduleGroupsPaginator", "ListSchedulesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListScheduleGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Paginator.ListScheduleGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/#listschedulegroupspaginator)
    """

    def paginate(
        self, *, NamePrefix: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListScheduleGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Paginator.ListScheduleGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/#listschedulegroupspaginator)
        """

class ListSchedulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Paginator.ListSchedules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/#listschedulespaginator)
    """

    def paginate(
        self,
        *,
        GroupName: str = ...,
        NamePrefix: str = ...,
        State: ScheduleStateType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSchedulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Paginator.ListSchedules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/#listschedulespaginator)
        """
