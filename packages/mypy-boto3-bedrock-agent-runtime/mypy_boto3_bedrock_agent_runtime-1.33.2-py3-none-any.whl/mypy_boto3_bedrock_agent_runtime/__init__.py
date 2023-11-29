"""
Main interface for bedrock-agent-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bedrock_agent_runtime import (
        AgentsforBedrockRuntimeClient,
        Client,
        RetrievePaginator,
    )

    session = Session()
    client: AgentsforBedrockRuntimeClient = session.client("bedrock-agent-runtime")

    retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```
"""

from .client import AgentsforBedrockRuntimeClient
from .paginator import RetrievePaginator

Client = AgentsforBedrockRuntimeClient


__all__ = ("AgentsforBedrockRuntimeClient", "Client", "RetrievePaginator")
