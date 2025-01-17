from pymongo.cursor import Cursor

from fast_seeker.core.pagination import LimitOffsetPaginator, LimitOffsetQuery, PageNumberPaginator, PageNumberQuery


def pymongo_limit_offset_translator(query: LimitOffsetQuery) -> LimitOffsetQuery:
    return query


def pymongo_page_number_translator(query: PageNumberQuery) -> LimitOffsetQuery:
    return LimitOffsetQuery(limit=query.size, offset=(query.page - 1) * query.size)


def pymongo_pagination_executor(data: Cursor, args: LimitOffsetQuery) -> Cursor:
    return data.limit(args.limit).skip(args.offset)


class PyMongoLimitOffsetPaginator(LimitOffsetPaginator[Cursor, Cursor, LimitOffsetQuery]):
    def __init__(self):
        super().__init__(translator=pymongo_limit_offset_translator, executor=pymongo_pagination_executor)


class PyMongoPageNumberPaginator(PageNumberPaginator[Cursor, Cursor, LimitOffsetQuery]):
    def __init__(self):
        super().__init__(translator=pymongo_page_number_translator, executor=pymongo_pagination_executor)
