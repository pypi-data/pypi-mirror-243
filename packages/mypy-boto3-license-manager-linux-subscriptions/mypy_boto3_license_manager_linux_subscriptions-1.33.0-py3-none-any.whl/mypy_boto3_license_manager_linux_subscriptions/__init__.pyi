"""
Main interface for license-manager-linux-subscriptions service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_license_manager_linux_subscriptions import (
        Client,
        LicenseManagerLinuxSubscriptionsClient,
        ListLinuxSubscriptionInstancesPaginator,
        ListLinuxSubscriptionsPaginator,
    )

    session = Session()
    client: LicenseManagerLinuxSubscriptionsClient = session.client("license-manager-linux-subscriptions")

    list_linux_subscription_instances_paginator: ListLinuxSubscriptionInstancesPaginator = client.get_paginator("list_linux_subscription_instances")
    list_linux_subscriptions_paginator: ListLinuxSubscriptionsPaginator = client.get_paginator("list_linux_subscriptions")
    ```
"""

from .client import LicenseManagerLinuxSubscriptionsClient
from .paginator import ListLinuxSubscriptionInstancesPaginator, ListLinuxSubscriptionsPaginator

Client = LicenseManagerLinuxSubscriptionsClient

__all__ = (
    "Client",
    "LicenseManagerLinuxSubscriptionsClient",
    "ListLinuxSubscriptionInstancesPaginator",
    "ListLinuxSubscriptionsPaginator",
)
