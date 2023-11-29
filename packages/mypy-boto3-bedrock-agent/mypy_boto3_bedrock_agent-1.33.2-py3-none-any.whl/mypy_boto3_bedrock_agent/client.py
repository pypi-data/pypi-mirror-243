"""
Type annotations for bedrock-agent service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bedrock_agent.client import AgentsforBedrockClient

    session = Session()
    client: AgentsforBedrockClient = session.client("bedrock-agent")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ActionGroupStateType, KnowledgeBaseStateType
from .paginator import (
    ListAgentActionGroupsPaginator,
    ListAgentAliasesPaginator,
    ListAgentKnowledgeBasesPaginator,
    ListAgentsPaginator,
    ListAgentVersionsPaginator,
    ListDataSourcesPaginator,
    ListIngestionJobsPaginator,
    ListKnowledgeBasesPaginator,
)
from .type_defs import (
    ActionGroupExecutorTypeDef,
    AgentAliasRoutingConfigurationListItemTypeDef,
    APISchemaTypeDef,
    AssociateAgentKnowledgeBaseResponseTypeDef,
    CreateAgentActionGroupResponseTypeDef,
    CreateAgentAliasResponseTypeDef,
    CreateAgentResponseTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateKnowledgeBaseResponseTypeDef,
    DataSourceConfigurationTypeDef,
    DeleteAgentAliasResponseTypeDef,
    DeleteAgentResponseTypeDef,
    DeleteAgentVersionResponseTypeDef,
    DeleteDataSourceResponseTypeDef,
    DeleteKnowledgeBaseResponseTypeDef,
    GetAgentActionGroupResponseTypeDef,
    GetAgentAliasResponseTypeDef,
    GetAgentKnowledgeBaseResponseTypeDef,
    GetAgentResponseTypeDef,
    GetAgentVersionResponseTypeDef,
    GetDataSourceResponseTypeDef,
    GetIngestionJobResponseTypeDef,
    GetKnowledgeBaseResponseTypeDef,
    IngestionJobFilterTypeDef,
    IngestionJobSortByTypeDef,
    KnowledgeBaseConfigurationTypeDef,
    ListAgentActionGroupsResponseTypeDef,
    ListAgentAliasesResponseTypeDef,
    ListAgentKnowledgeBasesResponseTypeDef,
    ListAgentsResponseTypeDef,
    ListAgentVersionsResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListIngestionJobsResponseTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PrepareAgentResponseTypeDef,
    PromptOverrideConfigurationTypeDef,
    ServerSideEncryptionConfigurationTypeDef,
    StartIngestionJobResponseTypeDef,
    StorageConfigurationTypeDef,
    UpdateAgentActionGroupResponseTypeDef,
    UpdateAgentAliasResponseTypeDef,
    UpdateAgentKnowledgeBaseResponseTypeDef,
    UpdateAgentResponseTypeDef,
    UpdateDataSourceResponseTypeDef,
    UpdateKnowledgeBaseResponseTypeDef,
    VectorIngestionConfigurationTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AgentsforBedrockClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AgentsforBedrockClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AgentsforBedrockClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#exceptions)
        """

    def associate_agent_knowledge_base(
        self,
        *,
        agentId: str,
        agentVersion: str,
        knowledgeBaseId: str,
        description: str,
        knowledgeBaseState: KnowledgeBaseStateType = ...
    ) -> AssociateAgentKnowledgeBaseResponseTypeDef:
        """
        Associate a Knowledge Base to an existing Amazon Bedrock Agent See also: [AWS
        API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/AssociateAgentKnowledgeBase).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.associate_agent_knowledge_base)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#associate_agent_knowledge_base)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#close)
        """

    def create_agent(
        self,
        *,
        agentName: str,
        agentResourceRoleArn: str,
        clientToken: str = ...,
        instruction: str = ...,
        foundationModel: str = ...,
        description: str = ...,
        idleSessionTTLInSeconds: int = ...,
        customerEncryptionKeyArn: str = ...,
        tags: Mapping[str, str] = ...,
        promptOverrideConfiguration: PromptOverrideConfigurationTypeDef = ...
    ) -> CreateAgentResponseTypeDef:
        """
        Creates an Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/CreateAgent).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_agent)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#create_agent)
        """

    def create_agent_action_group(
        self,
        *,
        agentId: str,
        agentVersion: str,
        actionGroupName: str,
        clientToken: str = ...,
        description: str = ...,
        parentActionGroupSignature: Literal["AMAZON.UserInput"] = ...,
        actionGroupExecutor: ActionGroupExecutorTypeDef = ...,
        apiSchema: APISchemaTypeDef = ...,
        actionGroupState: ActionGroupStateType = ...
    ) -> CreateAgentActionGroupResponseTypeDef:
        """
        Creates an Action Group for existing Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/CreateAgentActionGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_agent_action_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#create_agent_action_group)
        """

    def create_agent_alias(
        self,
        *,
        agentId: str,
        agentAliasName: str,
        clientToken: str = ...,
        description: str = ...,
        routingConfiguration: Sequence[AgentAliasRoutingConfigurationListItemTypeDef] = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateAgentAliasResponseTypeDef:
        """
        Creates an Alias for an existing Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/CreateAgentAlias).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_agent_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#create_agent_alias)
        """

    def create_data_source(
        self,
        *,
        knowledgeBaseId: str,
        name: str,
        dataSourceConfiguration: DataSourceConfigurationTypeDef,
        clientToken: str = ...,
        description: str = ...,
        serverSideEncryptionConfiguration: ServerSideEncryptionConfigurationTypeDef = ...,
        vectorIngestionConfiguration: VectorIngestionConfigurationTypeDef = ...
    ) -> CreateDataSourceResponseTypeDef:
        """
        Create a new data source See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/CreateDataSource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#create_data_source)
        """

    def create_knowledge_base(
        self,
        *,
        name: str,
        roleArn: str,
        knowledgeBaseConfiguration: KnowledgeBaseConfigurationTypeDef,
        storageConfiguration: StorageConfigurationTypeDef,
        clientToken: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateKnowledgeBaseResponseTypeDef:
        """
        Create a new knowledge base See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/CreateKnowledgeBase).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_knowledge_base)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#create_knowledge_base)
        """

    def delete_agent(
        self, *, agentId: str, skipResourceInUseCheck: bool = ...
    ) -> DeleteAgentResponseTypeDef:
        """
        Deletes an Agent for existing Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/DeleteAgent).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_agent)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#delete_agent)
        """

    def delete_agent_action_group(
        self,
        *,
        agentId: str,
        agentVersion: str,
        actionGroupId: str,
        skipResourceInUseCheck: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes an Action Group for existing Amazon Bedrock Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_agent_action_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#delete_agent_action_group)
        """

    def delete_agent_alias(
        self, *, agentId: str, agentAliasId: str
    ) -> DeleteAgentAliasResponseTypeDef:
        """
        Deletes an Alias for a Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/DeleteAgentAlias).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_agent_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#delete_agent_alias)
        """

    def delete_agent_version(
        self, *, agentId: str, agentVersion: str, skipResourceInUseCheck: bool = ...
    ) -> DeleteAgentVersionResponseTypeDef:
        """
        Deletes an Agent version for existing Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/DeleteAgentVersion).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_agent_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#delete_agent_version)
        """

    def delete_data_source(
        self, *, knowledgeBaseId: str, dataSourceId: str
    ) -> DeleteDataSourceResponseTypeDef:
        """
        Delete an existing data source See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/DeleteDataSource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#delete_data_source)
        """

    def delete_knowledge_base(self, *, knowledgeBaseId: str) -> DeleteKnowledgeBaseResponseTypeDef:
        """
        Delete an existing knowledge base See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/DeleteKnowledgeBase).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_knowledge_base)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#delete_knowledge_base)
        """

    def disassociate_agent_knowledge_base(
        self, *, agentId: str, agentVersion: str, knowledgeBaseId: str
    ) -> Dict[str, Any]:
        """
        Disassociate an existing Knowledge Base from an Amazon Bedrock Agent See also:
        [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/DisassociateAgentKnowledgeBase).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.disassociate_agent_knowledge_base)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#disassociate_agent_knowledge_base)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#generate_presigned_url)
        """

    def get_agent(self, *, agentId: str) -> GetAgentResponseTypeDef:
        """
        Gets an Agent for existing Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/GetAgent).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_agent)
        """

    def get_agent_action_group(
        self, *, agentId: str, agentVersion: str, actionGroupId: str
    ) -> GetAgentActionGroupResponseTypeDef:
        """
        Gets an Action Group for existing Amazon Bedrock Agent Version See also: [AWS
        API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/GetAgentActionGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent_action_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_agent_action_group)
        """

    def get_agent_alias(self, *, agentId: str, agentAliasId: str) -> GetAgentAliasResponseTypeDef:
        """
        Describes an Alias for a Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/GetAgentAlias).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_agent_alias)
        """

    def get_agent_knowledge_base(
        self, *, agentId: str, agentVersion: str, knowledgeBaseId: str
    ) -> GetAgentKnowledgeBaseResponseTypeDef:
        """
        Gets a knowledge base associated to an existing Amazon Bedrock Agent Version
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/GetAgentKnowledgeBase).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent_knowledge_base)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_agent_knowledge_base)
        """

    def get_agent_version(
        self, *, agentId: str, agentVersion: str
    ) -> GetAgentVersionResponseTypeDef:
        """
        Gets an Agent version for existing Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/GetAgentVersion).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_agent_version)
        """

    def get_data_source(
        self, *, knowledgeBaseId: str, dataSourceId: str
    ) -> GetDataSourceResponseTypeDef:
        """
        Get an existing data source See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/GetDataSource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_data_source)
        """

    def get_ingestion_job(
        self, *, knowledgeBaseId: str, dataSourceId: str, ingestionJobId: str
    ) -> GetIngestionJobResponseTypeDef:
        """
        Get an ingestion job See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/GetIngestionJob).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_ingestion_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_ingestion_job)
        """

    def get_knowledge_base(self, *, knowledgeBaseId: str) -> GetKnowledgeBaseResponseTypeDef:
        """
        Get an existing knowledge base See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/GetKnowledgeBase).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_knowledge_base)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_knowledge_base)
        """

    def list_agent_action_groups(
        self, *, agentId: str, agentVersion: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentActionGroupsResponseTypeDef:
        """
        Lists an Action Group for existing Amazon Bedrock Agent Version See also: [AWS
        API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/ListAgentActionGroups).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agent_action_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#list_agent_action_groups)
        """

    def list_agent_aliases(
        self, *, agentId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentAliasesResponseTypeDef:
        """
        Lists all the Aliases for an Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/ListAgentAliases).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agent_aliases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#list_agent_aliases)
        """

    def list_agent_knowledge_bases(
        self, *, agentId: str, agentVersion: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentKnowledgeBasesResponseTypeDef:
        """
        List of Knowledge Bases associated to an existing Amazon Bedrock Agent Version
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/ListAgentKnowledgeBases).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agent_knowledge_bases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#list_agent_knowledge_bases)
        """

    def list_agent_versions(
        self, *, agentId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentVersionsResponseTypeDef:
        """
        Lists Agent Versions See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/ListAgentVersions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agent_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#list_agent_versions)
        """

    def list_agents(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentsResponseTypeDef:
        """
        Lists Agents See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/ListAgents).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agents)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#list_agents)
        """

    def list_data_sources(
        self, *, knowledgeBaseId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListDataSourcesResponseTypeDef:
        """
        List data sources See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/ListDataSources).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_data_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#list_data_sources)
        """

    def list_ingestion_jobs(
        self,
        *,
        knowledgeBaseId: str,
        dataSourceId: str,
        filters: Sequence[IngestionJobFilterTypeDef] = ...,
        sortBy: IngestionJobSortByTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListIngestionJobsResponseTypeDef:
        """
        List ingestion jobs See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/ListIngestionJobs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_ingestion_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#list_ingestion_jobs)
        """

    def list_knowledge_bases(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListKnowledgeBasesResponseTypeDef:
        """
        List Knowledge Bases See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/ListKnowledgeBases).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_knowledge_bases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#list_knowledge_bases)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        List tags for a resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/ListTagsForResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#list_tags_for_resource)
        """

    def prepare_agent(self, *, agentId: str) -> PrepareAgentResponseTypeDef:
        """
        Prepares an existing Amazon Bedrock Agent to receive runtime requests See also:
        [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/PrepareAgent).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.prepare_agent)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#prepare_agent)
        """

    def start_ingestion_job(
        self,
        *,
        knowledgeBaseId: str,
        dataSourceId: str,
        clientToken: str = ...,
        description: str = ...
    ) -> StartIngestionJobResponseTypeDef:
        """
        Start a new ingestion job See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/StartIngestionJob).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.start_ingestion_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#start_ingestion_job)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tag a resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/TagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Untag a resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/UntagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#untag_resource)
        """

    def update_agent(
        self,
        *,
        agentId: str,
        agentName: str,
        agentResourceRoleArn: str,
        instruction: str = ...,
        foundationModel: str = ...,
        description: str = ...,
        idleSessionTTLInSeconds: int = ...,
        customerEncryptionKeyArn: str = ...,
        promptOverrideConfiguration: PromptOverrideConfigurationTypeDef = ...
    ) -> UpdateAgentResponseTypeDef:
        """
        Updates an existing Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/UpdateAgent).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_agent)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#update_agent)
        """

    def update_agent_action_group(
        self,
        *,
        agentId: str,
        agentVersion: str,
        actionGroupId: str,
        actionGroupName: str,
        description: str = ...,
        parentActionGroupSignature: Literal["AMAZON.UserInput"] = ...,
        actionGroupExecutor: ActionGroupExecutorTypeDef = ...,
        actionGroupState: ActionGroupStateType = ...,
        apiSchema: APISchemaTypeDef = ...
    ) -> UpdateAgentActionGroupResponseTypeDef:
        """
        Updates an existing Action Group for Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/UpdateAgentActionGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_agent_action_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#update_agent_action_group)
        """

    def update_agent_alias(
        self,
        *,
        agentId: str,
        agentAliasId: str,
        agentAliasName: str,
        description: str = ...,
        routingConfiguration: Sequence[AgentAliasRoutingConfigurationListItemTypeDef] = ...
    ) -> UpdateAgentAliasResponseTypeDef:
        """
        Updates an existing Alias for an Amazon Bedrock Agent See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/UpdateAgentAlias).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_agent_alias)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#update_agent_alias)
        """

    def update_agent_knowledge_base(
        self,
        *,
        agentId: str,
        agentVersion: str,
        knowledgeBaseId: str,
        description: str = ...,
        knowledgeBaseState: KnowledgeBaseStateType = ...
    ) -> UpdateAgentKnowledgeBaseResponseTypeDef:
        """
        Updates an existing Knowledge Base associated to an Amazon Bedrock Agent See
        also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/UpdateAgentKnowledgeBase).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_agent_knowledge_base)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#update_agent_knowledge_base)
        """

    def update_data_source(
        self,
        *,
        knowledgeBaseId: str,
        dataSourceId: str,
        name: str,
        dataSourceConfiguration: DataSourceConfigurationTypeDef,
        description: str = ...,
        serverSideEncryptionConfiguration: ServerSideEncryptionConfigurationTypeDef = ...,
        vectorIngestionConfiguration: VectorIngestionConfigurationTypeDef = ...
    ) -> UpdateDataSourceResponseTypeDef:
        """
        Update an existing data source See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/UpdateDataSource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#update_data_source)
        """

    def update_knowledge_base(
        self,
        *,
        knowledgeBaseId: str,
        name: str,
        roleArn: str,
        knowledgeBaseConfiguration: KnowledgeBaseConfigurationTypeDef,
        storageConfiguration: StorageConfigurationTypeDef,
        description: str = ...
    ) -> UpdateKnowledgeBaseResponseTypeDef:
        """
        Update an existing knowledge base See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/bedrock-agent-2023-06-05/UpdateKnowledgeBase).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_knowledge_base)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#update_knowledge_base)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_agent_action_groups"]
    ) -> ListAgentActionGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_agent_aliases"]
    ) -> ListAgentAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_agent_knowledge_bases"]
    ) -> ListAgentKnowledgeBasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_agent_versions"]
    ) -> ListAgentVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_agents"]) -> ListAgentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ingestion_jobs"]
    ) -> ListIngestionJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_knowledge_bases"]
    ) -> ListKnowledgeBasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/client/#get_paginator)
        """
