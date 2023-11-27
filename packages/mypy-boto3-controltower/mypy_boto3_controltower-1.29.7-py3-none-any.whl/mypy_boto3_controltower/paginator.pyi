"""
Type annotations for controltower service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_controltower.client import ControlTowerClient
    from mypy_boto3_controltower.paginator import (
        ListEnabledControlsPaginator,
        ListLandingZonesPaginator,
    )

    session = Session()
    client: ControlTowerClient = session.client("controltower")

    list_enabled_controls_paginator: ListEnabledControlsPaginator = client.get_paginator("list_enabled_controls")
    list_landing_zones_paginator: ListLandingZonesPaginator = client.get_paginator("list_landing_zones")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEnabledControlsOutputTypeDef,
    ListLandingZonesOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListEnabledControlsPaginator", "ListLandingZonesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListEnabledControlsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Paginator.ListEnabledControls)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listenabledcontrolspaginator)
    """

    def paginate(
        self, *, targetIdentifier: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnabledControlsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Paginator.ListEnabledControls.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listenabledcontrolspaginator)
        """

class ListLandingZonesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Paginator.ListLandingZones)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listlandingzonespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLandingZonesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Paginator.ListLandingZones.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/paginators/#listlandingzonespaginator)
        """
