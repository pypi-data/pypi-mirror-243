"""
Type annotations for trustedadvisor service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_trustedadvisor.client import TrustedAdvisorPublicAPIClient
    from mypy_boto3_trustedadvisor.paginator import (
        ListChecksPaginator,
        ListOrganizationRecommendationAccountsPaginator,
        ListOrganizationRecommendationResourcesPaginator,
        ListOrganizationRecommendationsPaginator,
        ListRecommendationResourcesPaginator,
        ListRecommendationsPaginator,
    )

    session = Session()
    client: TrustedAdvisorPublicAPIClient = session.client("trustedadvisor")

    list_checks_paginator: ListChecksPaginator = client.get_paginator("list_checks")
    list_organization_recommendation_accounts_paginator: ListOrganizationRecommendationAccountsPaginator = client.get_paginator("list_organization_recommendation_accounts")
    list_organization_recommendation_resources_paginator: ListOrganizationRecommendationResourcesPaginator = client.get_paginator("list_organization_recommendation_resources")
    list_organization_recommendations_paginator: ListOrganizationRecommendationsPaginator = client.get_paginator("list_organization_recommendations")
    list_recommendation_resources_paginator: ListRecommendationResourcesPaginator = client.get_paginator("list_recommendation_resources")
    list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import (
    RecommendationLanguageType,
    RecommendationPillarType,
    RecommendationSourceType,
    RecommendationStatusType,
    RecommendationTypeType,
    ResourceStatusType,
)
from .type_defs import (
    ListChecksResponseTypeDef,
    ListOrganizationRecommendationAccountsResponseTypeDef,
    ListOrganizationRecommendationResourcesResponseTypeDef,
    ListOrganizationRecommendationsResponseTypeDef,
    ListRecommendationResourcesResponseTypeDef,
    ListRecommendationsResponseTypeDef,
    PaginatorConfigTypeDef,
    TimestampTypeDef,
)

__all__ = (
    "ListChecksPaginator",
    "ListOrganizationRecommendationAccountsPaginator",
    "ListOrganizationRecommendationResourcesPaginator",
    "ListOrganizationRecommendationsPaginator",
    "ListRecommendationResourcesPaginator",
    "ListRecommendationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChecksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListChecks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listcheckspaginator)
    """

    def paginate(
        self,
        *,
        awsService: str = ...,
        language: RecommendationLanguageType = ...,
        pillar: RecommendationPillarType = ...,
        source: RecommendationSourceType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListChecks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listcheckspaginator)
        """


class ListOrganizationRecommendationAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendationAccounts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listorganizationrecommendationaccountspaginator)
    """

    def paginate(
        self,
        *,
        organizationRecommendationIdentifier: str,
        affectedAccountId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOrganizationRecommendationAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendationAccounts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listorganizationrecommendationaccountspaginator)
        """


class ListOrganizationRecommendationResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendationResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listorganizationrecommendationresourcespaginator)
    """

    def paginate(
        self,
        *,
        organizationRecommendationIdentifier: str,
        affectedAccountId: str = ...,
        regionCode: str = ...,
        status: ResourceStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOrganizationRecommendationResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendationResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listorganizationrecommendationresourcespaginator)
        """


class ListOrganizationRecommendationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listorganizationrecommendationspaginator)
    """

    def paginate(
        self,
        *,
        afterLastUpdatedAt: TimestampTypeDef = ...,
        awsService: str = ...,
        beforeLastUpdatedAt: TimestampTypeDef = ...,
        checkIdentifier: str = ...,
        pillar: RecommendationPillarType = ...,
        source: RecommendationSourceType = ...,
        status: RecommendationStatusType = ...,
        type: RecommendationTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOrganizationRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listorganizationrecommendationspaginator)
        """


class ListRecommendationResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListRecommendationResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listrecommendationresourcespaginator)
    """

    def paginate(
        self,
        *,
        recommendationIdentifier: str,
        regionCode: str = ...,
        status: ResourceStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecommendationResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListRecommendationResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listrecommendationresourcespaginator)
        """


class ListRecommendationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListRecommendations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listrecommendationspaginator)
    """

    def paginate(
        self,
        *,
        afterLastUpdatedAt: TimestampTypeDef = ...,
        awsService: str = ...,
        beforeLastUpdatedAt: TimestampTypeDef = ...,
        checkIdentifier: str = ...,
        pillar: RecommendationPillarType = ...,
        source: RecommendationSourceType = ...,
        status: RecommendationStatusType = ...,
        type: RecommendationTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor.html#TrustedAdvisorPublicAPI.Paginator.ListRecommendations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_trustedadvisor/paginators/#listrecommendationspaginator)
        """
