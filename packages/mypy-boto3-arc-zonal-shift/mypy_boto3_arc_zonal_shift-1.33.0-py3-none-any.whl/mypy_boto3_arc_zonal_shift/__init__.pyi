"""
Main interface for arc-zonal-shift service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_arc_zonal_shift import (
        ARCZonalShiftClient,
        Client,
        ListManagedResourcesPaginator,
        ListZonalShiftsPaginator,
    )

    session = Session()
    client: ARCZonalShiftClient = session.client("arc-zonal-shift")

    list_managed_resources_paginator: ListManagedResourcesPaginator = client.get_paginator("list_managed_resources")
    list_zonal_shifts_paginator: ListZonalShiftsPaginator = client.get_paginator("list_zonal_shifts")
    ```
"""

from .client import ARCZonalShiftClient
from .paginator import ListManagedResourcesPaginator, ListZonalShiftsPaginator

Client = ARCZonalShiftClient

__all__ = (
    "ARCZonalShiftClient",
    "Client",
    "ListManagedResourcesPaginator",
    "ListZonalShiftsPaginator",
)
