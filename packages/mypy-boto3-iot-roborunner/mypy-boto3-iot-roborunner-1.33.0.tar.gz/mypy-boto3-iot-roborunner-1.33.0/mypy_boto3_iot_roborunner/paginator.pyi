"""
Type annotations for iot-roborunner service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iot_roborunner.client import IoTRoboRunnerClient
    from mypy_boto3_iot_roborunner.paginator import (
        ListDestinationsPaginator,
        ListSitesPaginator,
        ListWorkerFleetsPaginator,
        ListWorkersPaginator,
    )

    session = Session()
    client: IoTRoboRunnerClient = session.client("iot-roborunner")

    list_destinations_paginator: ListDestinationsPaginator = client.get_paginator("list_destinations")
    list_sites_paginator: ListSitesPaginator = client.get_paginator("list_sites")
    list_worker_fleets_paginator: ListWorkerFleetsPaginator = client.get_paginator("list_worker_fleets")
    list_workers_paginator: ListWorkersPaginator = client.get_paginator("list_workers")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import DestinationStateType
from .type_defs import (
    ListDestinationsResponseTypeDef,
    ListSitesResponseTypeDef,
    ListWorkerFleetsResponseTypeDef,
    ListWorkersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListDestinationsPaginator",
    "ListSitesPaginator",
    "ListWorkerFleetsPaginator",
    "ListWorkersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDestinationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Paginator.ListDestinations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/paginators/#listdestinationspaginator)
    """

    def paginate(
        self,
        *,
        site: str,
        state: DestinationStateType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Paginator.ListDestinations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/paginators/#listdestinationspaginator)
        """

class ListSitesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Paginator.ListSites)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/paginators/#listsitespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Paginator.ListSites.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/paginators/#listsitespaginator)
        """

class ListWorkerFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Paginator.ListWorkerFleets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/paginators/#listworkerfleetspaginator)
    """

    def paginate(
        self, *, site: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkerFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Paginator.ListWorkerFleets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/paginators/#listworkerfleetspaginator)
        """

class ListWorkersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Paginator.ListWorkers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/paginators/#listworkerspaginator)
    """

    def paginate(
        self, *, site: str, fleet: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Paginator.ListWorkers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/paginators/#listworkerspaginator)
        """
