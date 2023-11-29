"""
Type annotations for chime-sdk-voice service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_chime_sdk_voice.client import ChimeSDKVoiceClient
    from mypy_boto3_chime_sdk_voice.paginator import (
        ListSipMediaApplicationsPaginator,
        ListSipRulesPaginator,
    )

    session = Session()
    client: ChimeSDKVoiceClient = session.client("chime-sdk-voice")

    list_sip_media_applications_paginator: ListSipMediaApplicationsPaginator = client.get_paginator("list_sip_media_applications")
    list_sip_rules_paginator: ListSipRulesPaginator = client.get_paginator("list_sip_rules")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListSipMediaApplicationsPaginator", "ListSipRulesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListSipMediaApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Paginator.ListSipMediaApplications)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/#listsipmediaapplicationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSipMediaApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Paginator.ListSipMediaApplications.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/#listsipmediaapplicationspaginator)
        """

class ListSipRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Paginator.ListSipRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/#listsiprulespaginator)
    """

    def paginate(
        self, *, SipMediaApplicationId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSipRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Paginator.ListSipRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/paginators/#listsiprulespaginator)
        """
