"""
Main interface for grafana service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_grafana import (
        Client,
        ListPermissionsPaginator,
        ListVersionsPaginator,
        ListWorkspacesPaginator,
        ManagedGrafanaClient,
    )

    session = Session()
    client: ManagedGrafanaClient = session.client("grafana")

    list_permissions_paginator: ListPermissionsPaginator = client.get_paginator("list_permissions")
    list_versions_paginator: ListVersionsPaginator = client.get_paginator("list_versions")
    list_workspaces_paginator: ListWorkspacesPaginator = client.get_paginator("list_workspaces")
    ```
"""

from .client import ManagedGrafanaClient
from .paginator import ListPermissionsPaginator, ListVersionsPaginator, ListWorkspacesPaginator

Client = ManagedGrafanaClient


__all__ = (
    "Client",
    "ListPermissionsPaginator",
    "ListVersionsPaginator",
    "ListWorkspacesPaginator",
    "ManagedGrafanaClient",
)
