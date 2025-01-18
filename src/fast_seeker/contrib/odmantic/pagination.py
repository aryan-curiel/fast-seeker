from fast_seeker.core.base import QueryProcessor
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery

from .engines import ODManticFindQueryBuilder


def ODManticLimitOffsetTranslator(query: LimitOffsetQuery) -> LimitOffsetQuery:
    return query


def ODManticPageNumberTranslator(query: PageNumberQuery) -> LimitOffsetQuery:
    return LimitOffsetQuery(limit=query.size, offset=(query.page - 1) * query.size)


class ODManticLimitOffsetPaginator(
    QueryProcessor[ODManticFindQueryBuilder, ODManticFindQueryBuilder, LimitOffsetQuery]
):
    def translate(self, data: ODManticFindQueryBuilder, query: LimitOffsetQuery) -> LimitOffsetQuery:
        return query

    def execute(self, data: ODManticFindQueryBuilder, args: LimitOffsetQuery) -> ODManticFindQueryBuilder:
        return data.limit(args.limit).skip(args.offset)


class ODManticPageNumberPaginator(QueryProcessor[ODManticFindQueryBuilder, ODManticFindQueryBuilder, LimitOffsetQuery]):
    def translate(self, data: ODManticFindQueryBuilder, query: PageNumberQuery) -> LimitOffsetQuery:
        return LimitOffsetQuery(limit=query.size, offset=(query.page - 1) * query.size)

    def execute(self, data: ODManticFindQueryBuilder, args: LimitOffsetQuery) -> ODManticFindQueryBuilder:
        return data.limit(args.limit).skip(args.offset)
