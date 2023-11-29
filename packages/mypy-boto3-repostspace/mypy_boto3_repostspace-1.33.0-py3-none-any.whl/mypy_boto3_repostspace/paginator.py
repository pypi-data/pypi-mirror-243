"""
Type annotations for repostspace service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_repostspace/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_repostspace.client import rePostPrivateClient
    from mypy_boto3_repostspace.paginator import (
        ListSpacesPaginator,
    )

    session = Session()
    client: rePostPrivateClient = session.client("repostspace")

    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListSpacesOutputTypeDef, PaginatorConfigTypeDef

__all__ = ("ListSpacesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListSpacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#rePostPrivate.Paginator.ListSpaces)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_repostspace/paginators/#listspacespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#rePostPrivate.Paginator.ListSpaces.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_repostspace/paginators/#listspacespaginator)
        """
