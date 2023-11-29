"""
Type annotations for customer-profiles service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_customer_profiles.client import CustomerProfilesClient
    from mypy_boto3_customer_profiles.paginator import (
        ListEventStreamsPaginator,
    )

    session = Session()
    client: CustomerProfilesClient = session.client("customer-profiles")

    list_event_streams_paginator: ListEventStreamsPaginator = client.get_paginator("list_event_streams")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListEventStreamsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListEventStreamsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListEventStreamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles.html#CustomerProfiles.Paginator.ListEventStreams)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listeventstreamspaginator)
    """

    def paginate(
        self, *, DomainName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEventStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles.html#CustomerProfiles.Paginator.ListEventStreams.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_customer_profiles/paginators/#listeventstreamspaginator)
        """
