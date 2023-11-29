"""
Type annotations for iot-roborunner service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iot_roborunner.client import IoTRoboRunnerClient

    session = Session()
    client: IoTRoboRunnerClient = session.client("iot-roborunner")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import DestinationStateType
from .paginator import (
    ListDestinationsPaginator,
    ListSitesPaginator,
    ListWorkerFleetsPaginator,
    ListWorkersPaginator,
)
from .type_defs import (
    CreateDestinationResponseTypeDef,
    CreateSiteResponseTypeDef,
    CreateWorkerFleetResponseTypeDef,
    CreateWorkerResponseTypeDef,
    GetDestinationResponseTypeDef,
    GetSiteResponseTypeDef,
    GetWorkerFleetResponseTypeDef,
    GetWorkerResponseTypeDef,
    ListDestinationsResponseTypeDef,
    ListSitesResponseTypeDef,
    ListWorkerFleetsResponseTypeDef,
    ListWorkersResponseTypeDef,
    OrientationTypeDef,
    PositionCoordinatesTypeDef,
    UpdateDestinationResponseTypeDef,
    UpdateSiteResponseTypeDef,
    UpdateWorkerFleetResponseTypeDef,
    UpdateWorkerResponseTypeDef,
    VendorPropertiesTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("IoTRoboRunnerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IoTRoboRunnerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTRoboRunnerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#close)
        """

    def create_destination(
        self,
        *,
        name: str,
        site: str,
        clientToken: str = ...,
        state: DestinationStateType = ...,
        additionalFixedProperties: str = ...
    ) -> CreateDestinationResponseTypeDef:
        """
        Grants permission to create a destination See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/CreateDestination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.create_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#create_destination)
        """

    def create_site(
        self, *, name: str, countryCode: str, clientToken: str = ..., description: str = ...
    ) -> CreateSiteResponseTypeDef:
        """
        Grants permission to create a site See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/CreateSite).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.create_site)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#create_site)
        """

    def create_worker(
        self,
        *,
        name: str,
        fleet: str,
        clientToken: str = ...,
        additionalTransientProperties: str = ...,
        additionalFixedProperties: str = ...,
        vendorProperties: VendorPropertiesTypeDef = ...,
        position: PositionCoordinatesTypeDef = ...,
        orientation: OrientationTypeDef = ...
    ) -> CreateWorkerResponseTypeDef:
        """
        Grants permission to create a worker See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/CreateWorker).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.create_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#create_worker)
        """

    def create_worker_fleet(
        self, *, name: str, site: str, clientToken: str = ..., additionalFixedProperties: str = ...
    ) -> CreateWorkerFleetResponseTypeDef:
        """
        Grants permission to create a worker fleet See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/CreateWorkerFleet).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.create_worker_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#create_worker_fleet)
        """

    def delete_destination(self, *, id: str) -> Dict[str, Any]:
        """
        Grants permission to delete a destination See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/DeleteDestination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.delete_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#delete_destination)
        """

    def delete_site(self, *, id: str) -> Dict[str, Any]:
        """
        Grants permission to delete a site See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/DeleteSite).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.delete_site)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#delete_site)
        """

    def delete_worker(self, *, id: str) -> Dict[str, Any]:
        """
        Grants permission to delete a worker See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/DeleteWorker).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.delete_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#delete_worker)
        """

    def delete_worker_fleet(self, *, id: str) -> Dict[str, Any]:
        """
        Grants permission to delete a worker fleet See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/DeleteWorkerFleet).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.delete_worker_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#delete_worker_fleet)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#generate_presigned_url)
        """

    def get_destination(self, *, id: str) -> GetDestinationResponseTypeDef:
        """
        Grants permission to get a destination See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/GetDestination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.get_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#get_destination)
        """

    def get_site(self, *, id: str) -> GetSiteResponseTypeDef:
        """
        Grants permission to get a site See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/GetSite).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.get_site)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#get_site)
        """

    def get_worker(self, *, id: str) -> GetWorkerResponseTypeDef:
        """
        Grants permission to get a worker See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/GetWorker).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.get_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#get_worker)
        """

    def get_worker_fleet(self, *, id: str) -> GetWorkerFleetResponseTypeDef:
        """
        Grants permission to get a worker fleet See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/GetWorkerFleet).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.get_worker_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#get_worker_fleet)
        """

    def list_destinations(
        self,
        *,
        site: str,
        maxResults: int = ...,
        nextToken: str = ...,
        state: DestinationStateType = ...
    ) -> ListDestinationsResponseTypeDef:
        """
        Grants permission to list destinations See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/ListDestinations).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.list_destinations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#list_destinations)
        """

    def list_sites(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListSitesResponseTypeDef:
        """
        Grants permission to list sites See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/ListSites).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.list_sites)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#list_sites)
        """

    def list_worker_fleets(
        self, *, site: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkerFleetsResponseTypeDef:
        """
        Grants permission to list worker fleets See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/ListWorkerFleets).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.list_worker_fleets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#list_worker_fleets)
        """

    def list_workers(
        self, *, site: str, maxResults: int = ..., nextToken: str = ..., fleet: str = ...
    ) -> ListWorkersResponseTypeDef:
        """
        Grants permission to list workers See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/ListWorkers).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.list_workers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#list_workers)
        """

    def update_destination(
        self,
        *,
        id: str,
        name: str = ...,
        state: DestinationStateType = ...,
        additionalFixedProperties: str = ...
    ) -> UpdateDestinationResponseTypeDef:
        """
        Grants permission to update a destination See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/UpdateDestination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.update_destination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#update_destination)
        """

    def update_site(
        self, *, id: str, name: str = ..., countryCode: str = ..., description: str = ...
    ) -> UpdateSiteResponseTypeDef:
        """
        Grants permission to update a site See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/UpdateSite).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.update_site)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#update_site)
        """

    def update_worker(
        self,
        *,
        id: str,
        name: str = ...,
        additionalTransientProperties: str = ...,
        additionalFixedProperties: str = ...,
        vendorProperties: VendorPropertiesTypeDef = ...,
        position: PositionCoordinatesTypeDef = ...,
        orientation: OrientationTypeDef = ...
    ) -> UpdateWorkerResponseTypeDef:
        """
        Grants permission to update a worker See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/UpdateWorker).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.update_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#update_worker)
        """

    def update_worker_fleet(
        self, *, id: str, name: str = ..., additionalFixedProperties: str = ...
    ) -> UpdateWorkerFleetResponseTypeDef:
        """
        Grants permission to update a worker fleet See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iot-roborunner-2018-05-10/UpdateWorkerFleet).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.update_worker_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#update_worker_fleet)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_destinations"]
    ) -> ListDestinationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_sites"]) -> ListSitesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_worker_fleets"]
    ) -> ListWorkerFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workers"]) -> ListWorkersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-roborunner.html#IoTRoboRunner.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_roborunner/client/#get_paginator)
        """
