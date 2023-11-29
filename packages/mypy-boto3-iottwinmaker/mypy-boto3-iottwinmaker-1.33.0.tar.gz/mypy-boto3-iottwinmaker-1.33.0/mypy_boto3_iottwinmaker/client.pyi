"""
Type annotations for iottwinmaker service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iottwinmaker.client import IoTTwinMakerClient

    session = Session()
    client: IoTTwinMakerClient = session.client("iottwinmaker")
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import DestinationTypeType, OrderByTimeType, PricingModeType, SourceTypeType
from .type_defs import (
    BatchPutPropertyValuesResponseTypeDef,
    CancelMetadataTransferJobResponseTypeDef,
    ComponentRequestTypeDef,
    ComponentUpdateRequestTypeDef,
    CompositeComponentRequestTypeDef,
    CompositeComponentTypeRequestTypeDef,
    CompositeComponentUpdateRequestTypeDef,
    CreateComponentTypeResponseTypeDef,
    CreateEntityResponseTypeDef,
    CreateMetadataTransferJobResponseTypeDef,
    CreateSceneResponseTypeDef,
    CreateSyncJobResponseTypeDef,
    CreateWorkspaceResponseTypeDef,
    DeleteComponentTypeResponseTypeDef,
    DeleteEntityResponseTypeDef,
    DeleteSyncJobResponseTypeDef,
    DeleteWorkspaceResponseTypeDef,
    DestinationConfigurationTypeDef,
    ExecuteQueryResponseTypeDef,
    FunctionRequestTypeDef,
    GetComponentTypeResponseTypeDef,
    GetEntityResponseTypeDef,
    GetMetadataTransferJobResponseTypeDef,
    GetPricingPlanResponseTypeDef,
    GetPropertyValueHistoryResponseTypeDef,
    GetPropertyValueResponseTypeDef,
    GetSceneResponseTypeDef,
    GetSyncJobResponseTypeDef,
    GetWorkspaceResponseTypeDef,
    InterpolationParametersTypeDef,
    ListComponentsResponseTypeDef,
    ListComponentTypesFilterTypeDef,
    ListComponentTypesResponseTypeDef,
    ListEntitiesFilterTypeDef,
    ListEntitiesResponseTypeDef,
    ListMetadataTransferJobsFilterTypeDef,
    ListMetadataTransferJobsResponseTypeDef,
    ListPropertiesResponseTypeDef,
    ListScenesResponseTypeDef,
    ListSyncJobsResponseTypeDef,
    ListSyncResourcesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkspacesResponseTypeDef,
    ParentEntityUpdateRequestTypeDef,
    PropertyDefinitionRequestTypeDef,
    PropertyFilterTypeDef,
    PropertyGroupRequestTypeDef,
    PropertyValueEntryTypeDef,
    SourceConfigurationTypeDef,
    SyncResourceFilterTypeDef,
    TabularConditionsTypeDef,
    TimestampTypeDef,
    UpdateComponentTypeResponseTypeDef,
    UpdateEntityResponseTypeDef,
    UpdatePricingPlanResponseTypeDef,
    UpdateSceneResponseTypeDef,
    UpdateWorkspaceResponseTypeDef,
)

__all__ = ("IoTTwinMakerClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConnectorFailureException: Type[BotocoreClientError]
    ConnectorTimeoutException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    QueryTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class IoTTwinMakerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTTwinMakerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#exceptions)
        """

    def batch_put_property_values(
        self, *, workspaceId: str, entries: Sequence[PropertyValueEntryTypeDef]
    ) -> BatchPutPropertyValuesResponseTypeDef:
        """
        Sets values for multiple time series properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.batch_put_property_values)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#batch_put_property_values)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#can_paginate)
        """

    def cancel_metadata_transfer_job(
        self, *, metadataTransferJobId: str
    ) -> CancelMetadataTransferJobResponseTypeDef:
        """
        Cancels the metadata transfer job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.cancel_metadata_transfer_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#cancel_metadata_transfer_job)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#close)
        """

    def create_component_type(
        self,
        *,
        workspaceId: str,
        componentTypeId: str,
        isSingleton: bool = ...,
        description: str = ...,
        propertyDefinitions: Mapping[str, PropertyDefinitionRequestTypeDef] = ...,
        extendsFrom: Sequence[str] = ...,
        functions: Mapping[str, FunctionRequestTypeDef] = ...,
        tags: Mapping[str, str] = ...,
        propertyGroups: Mapping[str, PropertyGroupRequestTypeDef] = ...,
        componentTypeName: str = ...,
        compositeComponentTypes: Mapping[str, CompositeComponentTypeRequestTypeDef] = ...
    ) -> CreateComponentTypeResponseTypeDef:
        """
        Creates a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_component_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_component_type)
        """

    def create_entity(
        self,
        *,
        workspaceId: str,
        entityName: str,
        entityId: str = ...,
        description: str = ...,
        components: Mapping[str, ComponentRequestTypeDef] = ...,
        compositeComponents: Mapping[str, CompositeComponentRequestTypeDef] = ...,
        parentEntityId: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateEntityResponseTypeDef:
        """
        Creates an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_entity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_entity)
        """

    def create_metadata_transfer_job(
        self,
        *,
        sources: Sequence[SourceConfigurationTypeDef],
        destination: DestinationConfigurationTypeDef,
        metadataTransferJobId: str = ...,
        description: str = ...
    ) -> CreateMetadataTransferJobResponseTypeDef:
        """
        Creates a new metadata transfer job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_metadata_transfer_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_metadata_transfer_job)
        """

    def create_scene(
        self,
        *,
        workspaceId: str,
        sceneId: str,
        contentLocation: str,
        description: str = ...,
        capabilities: Sequence[str] = ...,
        tags: Mapping[str, str] = ...,
        sceneMetadata: Mapping[str, str] = ...
    ) -> CreateSceneResponseTypeDef:
        """
        Creates a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_scene)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_scene)
        """

    def create_sync_job(
        self, *, workspaceId: str, syncSource: str, syncRole: str, tags: Mapping[str, str] = ...
    ) -> CreateSyncJobResponseTypeDef:
        """
        This action creates a SyncJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_sync_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_sync_job)
        """

    def create_workspace(
        self,
        *,
        workspaceId: str,
        description: str = ...,
        s3Location: str = ...,
        role: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateWorkspaceResponseTypeDef:
        """
        Creates a workplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#create_workspace)
        """

    def delete_component_type(
        self, *, workspaceId: str, componentTypeId: str
    ) -> DeleteComponentTypeResponseTypeDef:
        """
        Deletes a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_component_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#delete_component_type)
        """

    def delete_entity(
        self, *, workspaceId: str, entityId: str, isRecursive: bool = ...
    ) -> DeleteEntityResponseTypeDef:
        """
        Deletes an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_entity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#delete_entity)
        """

    def delete_scene(self, *, workspaceId: str, sceneId: str) -> Dict[str, Any]:
        """
        Deletes a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_scene)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#delete_scene)
        """

    def delete_sync_job(self, *, workspaceId: str, syncSource: str) -> DeleteSyncJobResponseTypeDef:
        """
        Delete the SyncJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_sync_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#delete_sync_job)
        """

    def delete_workspace(self, *, workspaceId: str) -> DeleteWorkspaceResponseTypeDef:
        """
        Deletes a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#delete_workspace)
        """

    def execute_query(
        self, *, workspaceId: str, queryStatement: str, maxResults: int = ..., nextToken: str = ...
    ) -> ExecuteQueryResponseTypeDef:
        """
        Run queries to access information from your knowledge graph of entities within
        individual
        workspaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.execute_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#execute_query)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#generate_presigned_url)
        """

    def get_component_type(
        self, *, workspaceId: str, componentTypeId: str
    ) -> GetComponentTypeResponseTypeDef:
        """
        Retrieves information about a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_component_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_component_type)
        """

    def get_entity(self, *, workspaceId: str, entityId: str) -> GetEntityResponseTypeDef:
        """
        Retrieves information about an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_entity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_entity)
        """

    def get_metadata_transfer_job(
        self, *, metadataTransferJobId: str
    ) -> GetMetadataTransferJobResponseTypeDef:
        """
        Gets a nmetadata transfer job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_metadata_transfer_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_metadata_transfer_job)
        """

    def get_pricing_plan(self) -> GetPricingPlanResponseTypeDef:
        """
        Gets the pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_pricing_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_pricing_plan)
        """

    def get_property_value(
        self,
        *,
        selectedProperties: Sequence[str],
        workspaceId: str,
        componentName: str = ...,
        componentPath: str = ...,
        componentTypeId: str = ...,
        entityId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        propertyGroupName: str = ...,
        tabularConditions: TabularConditionsTypeDef = ...
    ) -> GetPropertyValueResponseTypeDef:
        """
        Gets the property values for a component, component type, entity, or workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_property_value)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_property_value)
        """

    def get_property_value_history(
        self,
        *,
        workspaceId: str,
        selectedProperties: Sequence[str],
        entityId: str = ...,
        componentName: str = ...,
        componentPath: str = ...,
        componentTypeId: str = ...,
        propertyFilters: Sequence[PropertyFilterTypeDef] = ...,
        startDateTime: TimestampTypeDef = ...,
        endDateTime: TimestampTypeDef = ...,
        interpolation: InterpolationParametersTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        orderByTime: OrderByTimeType = ...,
        startTime: str = ...,
        endTime: str = ...
    ) -> GetPropertyValueHistoryResponseTypeDef:
        """
        Retrieves information about the history of a time series property value for a
        component, component type, entity, or
        workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_property_value_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_property_value_history)
        """

    def get_scene(self, *, workspaceId: str, sceneId: str) -> GetSceneResponseTypeDef:
        """
        Retrieves information about a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_scene)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_scene)
        """

    def get_sync_job(self, *, syncSource: str, workspaceId: str = ...) -> GetSyncJobResponseTypeDef:
        """
        Gets the SyncJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_sync_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_sync_job)
        """

    def get_workspace(self, *, workspaceId: str) -> GetWorkspaceResponseTypeDef:
        """
        Retrieves information about a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#get_workspace)
        """

    def list_component_types(
        self,
        *,
        workspaceId: str,
        filters: Sequence[ListComponentTypesFilterTypeDef] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListComponentTypesResponseTypeDef:
        """
        Lists all component types in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_component_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_component_types)
        """

    def list_components(
        self,
        *,
        workspaceId: str,
        entityId: str,
        componentPath: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListComponentsResponseTypeDef:
        """
        This API lists the components of an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_components)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_components)
        """

    def list_entities(
        self,
        *,
        workspaceId: str,
        filters: Sequence[ListEntitiesFilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListEntitiesResponseTypeDef:
        """
        Lists all entities in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_entities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_entities)
        """

    def list_metadata_transfer_jobs(
        self,
        *,
        sourceType: SourceTypeType,
        destinationType: DestinationTypeType,
        filters: Sequence[ListMetadataTransferJobsFilterTypeDef] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListMetadataTransferJobsResponseTypeDef:
        """
        Lists the metadata transfer jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_metadata_transfer_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_metadata_transfer_jobs)
        """

    def list_properties(
        self,
        *,
        workspaceId: str,
        entityId: str,
        componentName: str = ...,
        componentPath: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListPropertiesResponseTypeDef:
        """
        This API lists the properties of a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_properties)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_properties)
        """

    def list_scenes(
        self, *, workspaceId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListScenesResponseTypeDef:
        """
        Lists all scenes in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_scenes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_scenes)
        """

    def list_sync_jobs(
        self, *, workspaceId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListSyncJobsResponseTypeDef:
        """
        List all SyncJobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_sync_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_sync_jobs)
        """

    def list_sync_resources(
        self,
        *,
        workspaceId: str,
        syncSource: str,
        filters: Sequence[SyncResourceFilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListSyncResourcesResponseTypeDef:
        """
        Lists the sync resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_sync_resources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_sync_resources)
        """

    def list_tags_for_resource(
        self, *, resourceARN: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_tags_for_resource)
        """

    def list_workspaces(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkspacesResponseTypeDef:
        """
        Retrieves information about workspaces in the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_workspaces)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#list_workspaces)
        """

    def tag_resource(self, *, resourceARN: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#tag_resource)
        """

    def untag_resource(self, *, resourceARN: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#untag_resource)
        """

    def update_component_type(
        self,
        *,
        workspaceId: str,
        componentTypeId: str,
        isSingleton: bool = ...,
        description: str = ...,
        propertyDefinitions: Mapping[str, PropertyDefinitionRequestTypeDef] = ...,
        extendsFrom: Sequence[str] = ...,
        functions: Mapping[str, FunctionRequestTypeDef] = ...,
        propertyGroups: Mapping[str, PropertyGroupRequestTypeDef] = ...,
        componentTypeName: str = ...,
        compositeComponentTypes: Mapping[str, CompositeComponentTypeRequestTypeDef] = ...
    ) -> UpdateComponentTypeResponseTypeDef:
        """
        Updates information in a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_component_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#update_component_type)
        """

    def update_entity(
        self,
        *,
        workspaceId: str,
        entityId: str,
        entityName: str = ...,
        description: str = ...,
        componentUpdates: Mapping[str, ComponentUpdateRequestTypeDef] = ...,
        compositeComponentUpdates: Mapping[str, CompositeComponentUpdateRequestTypeDef] = ...,
        parentEntityUpdate: ParentEntityUpdateRequestTypeDef = ...
    ) -> UpdateEntityResponseTypeDef:
        """
        Updates an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_entity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#update_entity)
        """

    def update_pricing_plan(
        self, *, pricingMode: PricingModeType, bundleNames: Sequence[str] = ...
    ) -> UpdatePricingPlanResponseTypeDef:
        """
        Update the pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_pricing_plan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#update_pricing_plan)
        """

    def update_scene(
        self,
        *,
        workspaceId: str,
        sceneId: str,
        contentLocation: str = ...,
        description: str = ...,
        capabilities: Sequence[str] = ...,
        sceneMetadata: Mapping[str, str] = ...
    ) -> UpdateSceneResponseTypeDef:
        """
        Updates a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_scene)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#update_scene)
        """

    def update_workspace(
        self, *, workspaceId: str, description: str = ..., role: str = ..., s3Location: str = ...
    ) -> UpdateWorkspaceResponseTypeDef:
        """
        Updates a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_workspace)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iottwinmaker/client/#update_workspace)
        """
