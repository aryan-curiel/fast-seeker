from typing import TypedDict

from beanie.odm.queries.find import FindMany

from fast_seeker.core.base import QueryExecutor, QueryTranslator
from fast_seeker.core.pagination import (
    LimitOffsetPaginator,
    LimitOffsetQuery,
    PageNumberPaginator,
    PageNumberQuery,
)


class BeanieQueryPage(TypedDict):
    limit: int
    skip: int


class BeanieLimitOffsetQueryTranslator(QueryTranslator[LimitOffsetQuery, BeanieQueryPage]):
    def __call__(self, *, query: LimitOffsetQuery, **kwargs) -> BeanieQueryPage:
        return BeanieQueryPage(limit=query.limit, skip=query.offset)


class BeaniePageNumberQueryTranslator(QueryTranslator[PageNumberQuery, BeanieQueryPage]):
    def __call__(self, *, query: PageNumberQuery, **kwargs) -> BeanieQueryPage:
        return BeanieQueryPage(limit=query.size, skip=(query.page - 1) * query.size)


class BeaniePaginationExecutor(QueryExecutor[FindMany, BeanieQueryPage]):
    def __call__(self, *, source: FindMany, translated_query: BeanieQueryPage, **kwargs) -> FindMany:
        return source.limit(translated_query["limit"]).skip(translated_query["skip"])


class BeanieLimitOffsetPaginator(LimitOffsetPaginator[FindMany, BeanieQueryPage]):
    translator = BeanieLimitOffsetQueryTranslator()
    executor = BeaniePaginationExecutor()


class BeaniePageNumberPaginator(PageNumberPaginator[FindMany, BeanieQueryPage]):
    translator = BeaniePageNumberQueryTranslator()
    executor = BeaniePaginationExecutor()
