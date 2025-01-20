from beanie.odm.queries.find import FindMany

from fast_seeker.core.pagination import LimitOffsetPaginator, LimitOffsetQuery, PageNumberPaginator, PageNumberQuery


class BeanieLimitOffsetPaginator(LimitOffsetPaginator[FindMany, FindMany, LimitOffsetQuery]):
    def translate(self, data: FindMany, query: LimitOffsetQuery) -> LimitOffsetQuery:
        return query

    def execute(self, data: FindMany, args: LimitOffsetQuery) -> FindMany:
        return data.limit(args.limit).skip(args.offset)


class BeaniePageNumberPaginator(PageNumberPaginator[FindMany, FindMany, LimitOffsetQuery]):
    def translate(self, data: FindMany, query: PageNumberQuery) -> LimitOffsetQuery:
        return LimitOffsetQuery(limit=query.size, offset=(query.page - 1) * query.size)

    def execute(self, data: FindMany, args: LimitOffsetQuery) -> FindMany:
        return data.limit(args.limit).skip(args.offset)
