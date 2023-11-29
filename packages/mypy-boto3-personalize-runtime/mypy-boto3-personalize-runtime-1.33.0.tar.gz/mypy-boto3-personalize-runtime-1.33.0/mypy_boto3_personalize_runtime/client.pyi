"""
Type annotations for personalize-runtime service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_personalize_runtime.client import PersonalizeRuntimeClient

    session = Session()
    client: PersonalizeRuntimeClient = session.client("personalize-runtime")
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    GetActionRecommendationsResponseTypeDef,
    GetPersonalizedRankingResponseTypeDef,
    GetRecommendationsResponseTypeDef,
    PromotionTypeDef,
)

__all__ = ("PersonalizeRuntimeClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class PersonalizeRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-runtime.html#PersonalizeRuntime.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PersonalizeRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client/#close)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client/#generate_presigned_url)
        """

    def get_action_recommendations(
        self,
        *,
        campaignArn: str = ...,
        userId: str = ...,
        numResults: int = ...,
        filterArn: str = ...,
        filterValues: Mapping[str, str] = ...
    ) -> GetActionRecommendationsResponseTypeDef:
        """
        Returns a list of recommended actions in sorted in descending order by
        prediction
        score.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.get_action_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client/#get_action_recommendations)
        """

    def get_personalized_ranking(
        self,
        *,
        campaignArn: str,
        inputList: Sequence[str],
        userId: str,
        context: Mapping[str, str] = ...,
        filterArn: str = ...,
        filterValues: Mapping[str, str] = ...,
        metadataColumns: Mapping[str, Sequence[str]] = ...
    ) -> GetPersonalizedRankingResponseTypeDef:
        """
        Re-ranks a list of recommended items for the given user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.get_personalized_ranking)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client/#get_personalized_ranking)
        """

    def get_recommendations(
        self,
        *,
        campaignArn: str = ...,
        itemId: str = ...,
        userId: str = ...,
        numResults: int = ...,
        context: Mapping[str, str] = ...,
        filterArn: str = ...,
        filterValues: Mapping[str, str] = ...,
        recommenderArn: str = ...,
        promotions: Sequence[PromotionTypeDef] = ...,
        metadataColumns: Mapping[str, Sequence[str]] = ...
    ) -> GetRecommendationsResponseTypeDef:
        """
        Returns a list of recommended items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.get_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client/#get_recommendations)
        """
