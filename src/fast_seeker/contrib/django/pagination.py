from django.db.models import QuerySet

from fast_seeker.core.base import QueryExecutor, QueryTranslator
from fast_seeker.core.pagination import (
    LimitOffsetPaginator,
    LimitOffsetQuery,
    PageNumberPaginator,
    PageNumberQuery,
)


class DjangoLimitOffsetQueryTranslator(QueryTranslator[LimitOffsetQuery, slice]):
    def __call__(self, *, query: LimitOffsetQuery, **kwargs) -> slice:
        return slice(query.offset, query.offset + query.limit)


class DjangoPageNumberQueryTranslator(QueryTranslator[PageNumberQuery, slice]):
    def __call__(self, *, query: PageNumberQuery, **kwargs) -> slice:
        return slice((query.page - 1) * query.size, query.page * query.size)


class DjangoPaginationExecutor(QueryExecutor[QuerySet, slice]):
    def __call__(self, *, source: QuerySet, translated_query: slice, **kwargs) -> QuerySet:
        return source[translated_query]


class DjangoLimitOffsetPaginator(LimitOffsetPaginator[QuerySet, slice]):
    translator = DjangoLimitOffsetQueryTranslator()
    executor = DjangoPaginationExecutor()


class DjangoPageNumberPaginator(PageNumberPaginator[QuerySet, slice]):
    translator = DjangoPageNumberQueryTranslator()
    executor = DjangoPaginationExecutor()
