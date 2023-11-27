"""
Main interface for repostspace service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_repostspace import (
        Client,
        ListSpacesPaginator,
        rePostPrivateClient,
    )

    session = Session()
    client: rePostPrivateClient = session.client("repostspace")

    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    ```
"""

from .client import rePostPrivateClient
from .paginator import ListSpacesPaginator

Client = rePostPrivateClient


__all__ = ("Client", "ListSpacesPaginator", "rePostPrivateClient")
