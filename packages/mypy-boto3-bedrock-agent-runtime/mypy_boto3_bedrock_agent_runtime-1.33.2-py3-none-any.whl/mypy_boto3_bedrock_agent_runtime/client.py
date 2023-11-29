"""
Type annotations for bedrock-agent-runtime service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient

    session = Session()
    client: AgentsforBedrockRuntimeClient = session.client("bedrock-agent-runtime")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import RetrievePaginator
from .type_defs import (
    InvokeAgentResponseTypeDef,
    KnowledgeBaseQueryTypeDef,
    KnowledgeBaseRetrievalConfigurationTypeDef,
    RetrieveAndGenerateConfigurationTypeDef,
    RetrieveAndGenerateInputTypeDef,
    RetrieveAndGenerateResponseTypeDef,
    RetrieveAndGenerateSessionConfigurationTypeDef,
    RetrieveResponseTypeDef,
    SessionStateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AgentsforBedrockRuntimeClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadGatewayException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailedException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AgentsforBedrockRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AgentsforBedrockRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/#close)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/#generate_presigned_url)
        """

    def invoke_agent(
        self,
        *,
        agentId: str,
        agentAliasId: str,
        sessionId: str,
        inputText: str,
        sessionState: SessionStateTypeDef = ...,
        endSession: bool = ...,
        enableTrace: bool = ...
    ) -> InvokeAgentResponseTypeDef:
        """
        Invokes the specified Bedrock model to run inference using the input provided
        in the request
        body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client.invoke_agent)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/#invoke_agent)
        """

    def retrieve(
        self,
        *,
        knowledgeBaseId: str,
        retrievalQuery: KnowledgeBaseQueryTypeDef,
        retrievalConfiguration: KnowledgeBaseRetrievalConfigurationTypeDef = ...,
        nextToken: str = ...
    ) -> RetrieveResponseTypeDef:
        """
        Retrieve from knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client.retrieve)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/#retrieve)
        """

    def retrieve_and_generate(
        self,
        *,
        input: RetrieveAndGenerateInputTypeDef,
        sessionId: str = ...,
        retrieveAndGenerateConfiguration: RetrieveAndGenerateConfigurationTypeDef = ...,
        sessionConfiguration: RetrieveAndGenerateSessionConfigurationTypeDef = ...
    ) -> RetrieveAndGenerateResponseTypeDef:
        """
        RetrieveAndGenerate API See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-runtime-2023-07-26/RetrieveAndGenerate).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client.retrieve_and_generate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/#retrieve_and_generate)
        """

    def get_paginator(self, operation_name: Literal["retrieve"]) -> RetrievePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/client/#get_paginator)
        """
