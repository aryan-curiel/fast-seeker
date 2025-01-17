from beanie.odm.queries.find import FindMany

from fast_seeker.core.pagination import LimitOffsetPaginator, LimitOffsetQuery, PageNumberPaginator, PageNumberQuery


def beanie_limit_offset_translator(query: LimitOffsetQuery) -> LimitOffsetQuery:
    return query


def beanie_page_number_translator(query: PageNumberQuery) -> LimitOffsetQuery:
    return LimitOffsetQuery(limit=query.size, offset=(query.page - 1) * query.size)


def beanie_pagination_executor(data: FindMany, args: LimitOffsetQuery) -> FindMany:
    return data.limit(args.limit).skip(args.offset)


class BeanieLimitOffsetPaginator(LimitOffsetPaginator[FindMany, FindMany, LimitOffsetQuery]):
    def __init__(self):
        super().__init__(translator=beanie_limit_offset_translator, executor=beanie_pagination_executor)


class BeaniePageNumberPaginator(PageNumberPaginator[FindMany, FindMany, LimitOffsetQuery]):
    def __init__(self):
        super().__init__(translator=beanie_page_number_translator, executor=beanie_pagination_executor)
