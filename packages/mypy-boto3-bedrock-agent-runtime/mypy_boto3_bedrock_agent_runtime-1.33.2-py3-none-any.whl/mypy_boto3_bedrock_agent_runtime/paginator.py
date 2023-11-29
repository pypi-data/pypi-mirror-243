"""
Type annotations for bedrock-agent-runtime service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
    from mypy_boto3_bedrock_agent_runtime.paginator import (
        RetrievePaginator,
    )

    session = Session()
    client: AgentsforBedrockRuntimeClient = session.client("bedrock-agent-runtime")

    retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    KnowledgeBaseQueryTypeDef,
    KnowledgeBaseRetrievalConfigurationTypeDef,
    PaginatorConfigTypeDef,
    RetrieveResponseTypeDef,
)

__all__ = ("RetrievePaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class RetrievePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Paginator.Retrieve)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/#retrievepaginator)
    """

    def paginate(
        self,
        *,
        knowledgeBaseId: str,
        retrievalQuery: KnowledgeBaseQueryTypeDef,
        retrievalConfiguration: KnowledgeBaseRetrievalConfigurationTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[RetrieveResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Paginator.Retrieve.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/#retrievepaginator)
        """
