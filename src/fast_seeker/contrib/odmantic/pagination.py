from fast_seeker.core.pagination import LimitOffsetPaginator, LimitOffsetQuery, PageNumberPaginator, PageNumberQuery

from .engines import ODManticFindQueryBuilder


class ODManticLimitOffsetPaginator(
    LimitOffsetPaginator[ODManticFindQueryBuilder, ODManticFindQueryBuilder, LimitOffsetQuery]
):
    def translate(self, data: ODManticFindQueryBuilder, query: LimitOffsetQuery) -> LimitOffsetQuery:
        return query

    def execute(self, data: ODManticFindQueryBuilder, args: LimitOffsetQuery) -> ODManticFindQueryBuilder:
        return data.limit(args.limit).skip(args.offset)


class ODManticPageNumberPaginator(
    PageNumberPaginator[ODManticFindQueryBuilder, ODManticFindQueryBuilder, LimitOffsetQuery]
):
    def translate(self, data: ODManticFindQueryBuilder, query: PageNumberQuery) -> LimitOffsetQuery:
        return LimitOffsetQuery(limit=query.size, offset=(query.page - 1) * query.size)

    def execute(self, data: ODManticFindQueryBuilder, args: LimitOffsetQuery) -> ODManticFindQueryBuilder:
        return data.limit(args.limit).skip(args.offset)
