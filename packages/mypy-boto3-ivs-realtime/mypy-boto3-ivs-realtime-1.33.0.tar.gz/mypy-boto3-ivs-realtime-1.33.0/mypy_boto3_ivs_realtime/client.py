"""
Type annotations for ivs-realtime service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ivs_realtime.client import ivsrealtimeClient

    session = Session()
    client: ivsrealtimeClient = session.client("ivs-realtime")
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import ParticipantStateType, ParticipantTokenCapabilityType
from .type_defs import (
    CreateEncoderConfigurationResponseTypeDef,
    CreateParticipantTokenResponseTypeDef,
    CreateStageResponseTypeDef,
    CreateStorageConfigurationResponseTypeDef,
    DestinationConfigurationTypeDef,
    GetCompositionResponseTypeDef,
    GetEncoderConfigurationResponseTypeDef,
    GetParticipantResponseTypeDef,
    GetStageResponseTypeDef,
    GetStageSessionResponseTypeDef,
    GetStorageConfigurationResponseTypeDef,
    LayoutConfigurationTypeDef,
    ListCompositionsResponseTypeDef,
    ListEncoderConfigurationsResponseTypeDef,
    ListParticipantEventsResponseTypeDef,
    ListParticipantsResponseTypeDef,
    ListStageSessionsResponseTypeDef,
    ListStagesResponseTypeDef,
    ListStorageConfigurationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ParticipantTokenConfigurationTypeDef,
    S3StorageConfigurationTypeDef,
    StartCompositionResponseTypeDef,
    UpdateStageResponseTypeDef,
    VideoTypeDef,
)

__all__ = ("ivsrealtimeClient",)


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
    PendingVerification: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ivsrealtimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ivsrealtimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#close)
        """

    def create_encoder_configuration(
        self, *, name: str = ..., tags: Mapping[str, str] = ..., video: VideoTypeDef = ...
    ) -> CreateEncoderConfigurationResponseTypeDef:
        """
        Creates an EncoderConfiguration object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.create_encoder_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#create_encoder_configuration)
        """

    def create_participant_token(
        self,
        *,
        stageArn: str,
        attributes: Mapping[str, str] = ...,
        capabilities: Sequence[ParticipantTokenCapabilityType] = ...,
        duration: int = ...,
        userId: str = ...
    ) -> CreateParticipantTokenResponseTypeDef:
        """
        Creates an additional token for a specified stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.create_participant_token)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#create_participant_token)
        """

    def create_stage(
        self,
        *,
        name: str = ...,
        participantTokenConfigurations: Sequence[ParticipantTokenConfigurationTypeDef] = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateStageResponseTypeDef:
        """
        Creates a new stage (and optionally participant tokens).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.create_stage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#create_stage)
        """

    def create_storage_configuration(
        self, *, s3: S3StorageConfigurationTypeDef, name: str = ..., tags: Mapping[str, str] = ...
    ) -> CreateStorageConfigurationResponseTypeDef:
        """
        Creates a new storage configuration, used to enable recording to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.create_storage_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#create_storage_configuration)
        """

    def delete_encoder_configuration(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes an EncoderConfiguration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.delete_encoder_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#delete_encoder_configuration)
        """

    def delete_stage(self, *, arn: str) -> Dict[str, Any]:
        """
        Shuts down and deletes the specified stage (disconnecting all participants).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.delete_stage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#delete_stage)
        """

    def delete_storage_configuration(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes the storage configuration for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.delete_storage_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#delete_storage_configuration)
        """

    def disconnect_participant(
        self, *, participantId: str, stageArn: str, reason: str = ...
    ) -> Dict[str, Any]:
        """
        Disconnects a specified participant and revokes the participant permanently
        from a specified
        stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.disconnect_participant)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#disconnect_participant)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#generate_presigned_url)
        """

    def get_composition(self, *, arn: str) -> GetCompositionResponseTypeDef:
        """
        Get information about the specified Composition resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.get_composition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#get_composition)
        """

    def get_encoder_configuration(self, *, arn: str) -> GetEncoderConfigurationResponseTypeDef:
        """
        Gets information about the specified EncoderConfiguration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.get_encoder_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#get_encoder_configuration)
        """

    def get_participant(
        self, *, participantId: str, sessionId: str, stageArn: str
    ) -> GetParticipantResponseTypeDef:
        """
        Gets information about the specified participant token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.get_participant)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#get_participant)
        """

    def get_stage(self, *, arn: str) -> GetStageResponseTypeDef:
        """
        Gets information for the specified stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.get_stage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#get_stage)
        """

    def get_stage_session(self, *, sessionId: str, stageArn: str) -> GetStageSessionResponseTypeDef:
        """
        Gets information for the specified stage session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.get_stage_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#get_stage_session)
        """

    def get_storage_configuration(self, *, arn: str) -> GetStorageConfigurationResponseTypeDef:
        """
        Gets the storage configuration for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.get_storage_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#get_storage_configuration)
        """

    def list_compositions(
        self,
        *,
        filterByEncoderConfigurationArn: str = ...,
        filterByStageArn: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListCompositionsResponseTypeDef:
        """
        Gets summary information about all Compositions in your account, in the AWS
        region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.list_compositions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#list_compositions)
        """

    def list_encoder_configurations(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListEncoderConfigurationsResponseTypeDef:
        """
        Gets summary information about all EncoderConfigurations in your account, in
        the AWS region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.list_encoder_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#list_encoder_configurations)
        """

    def list_participant_events(
        self,
        *,
        participantId: str,
        sessionId: str,
        stageArn: str,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListParticipantEventsResponseTypeDef:
        """
        Lists events for a specified participant that occurred during a specified stage
        session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.list_participant_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#list_participant_events)
        """

    def list_participants(
        self,
        *,
        sessionId: str,
        stageArn: str,
        filterByPublished: bool = ...,
        filterByState: ParticipantStateType = ...,
        filterByUserId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListParticipantsResponseTypeDef:
        """
        Lists all participants in a specified stage session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.list_participants)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#list_participants)
        """

    def list_stage_sessions(
        self, *, stageArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStageSessionsResponseTypeDef:
        """
        Gets all sessions for a specified stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.list_stage_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#list_stage_sessions)
        """

    def list_stages(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListStagesResponseTypeDef:
        """
        Gets summary information about all stages in your account, in the AWS region
        where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.list_stages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#list_stages)
        """

    def list_storage_configurations(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListStorageConfigurationsResponseTypeDef:
        """
        Gets summary information about all storage configurations in your account, in
        the AWS region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.list_storage_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#list_storage_configurations)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Gets information about AWS tags for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#list_tags_for_resource)
        """

    def start_composition(
        self,
        *,
        destinations: Sequence[DestinationConfigurationTypeDef],
        stageArn: str,
        idempotencyToken: str = ...,
        layout: LayoutConfigurationTypeDef = ...,
        tags: Mapping[str, str] = ...
    ) -> StartCompositionResponseTypeDef:
        """
        Starts a Composition from a stage based on the configuration provided in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.start_composition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#start_composition)
        """

    def stop_composition(self, *, arn: str) -> Dict[str, Any]:
        """
        Stops and deletes a Composition resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.stop_composition)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#stop_composition)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds or updates tags for the AWS resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from the resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#untag_resource)
        """

    def update_stage(self, *, arn: str, name: str = ...) -> UpdateStageResponseTypeDef:
        """
        Updates a stage’s configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#ivsrealtime.Client.update_stage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs_realtime/client/#update_stage)
        """
