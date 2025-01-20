from motor.core import AgnosticCursor as Cursor

from fast_seeker.core.pagination import LimitOffsetPaginator, LimitOffsetQuery, PageNumberPaginator, PageNumberQuery


class MotorLimitOffsetPaginator(LimitOffsetPaginator[Cursor, Cursor, LimitOffsetQuery]):
    def translate(self, data: Cursor, query: LimitOffsetQuery) -> LimitOffsetQuery:
        return query

    def execute(self, data: Cursor, args: LimitOffsetQuery) -> Cursor:
        return data.limit(args.limit).skip(args.offset)


class MotorPageNumberPaginator(PageNumberPaginator[Cursor, Cursor, LimitOffsetQuery]):
    def translate(self, data: Cursor, query: PageNumberQuery) -> LimitOffsetQuery:
        return LimitOffsetQuery(limit=query.size, offset=(query.page - 1) * query.size)

    def execute(self, data: Cursor, args: LimitOffsetQuery) -> Cursor:
        return data.limit(args.limit).skip(args.offset)
