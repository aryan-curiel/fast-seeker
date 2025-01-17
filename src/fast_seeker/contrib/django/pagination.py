from django.db.models import QuerySet

from fast_seeker.core.pagination import LimitOffsetPaginator, LimitOffsetQuery, PageNumberPaginator, PageNumberQuery


def django_limit_offset_translator(query: LimitOffsetQuery) -> slice:
    return slice(query.offset, query.offset + query.limit)


def django_page_number_translator(query: PageNumberQuery) -> slice:
    return slice((query.page - 1) * query.size, query.page * query.size)


def django_pagination_executor(data: QuerySet, args: slice) -> QuerySet:
    return data[args]


class QuerySetLimitOffsetPaginator(LimitOffsetPaginator[QuerySet, QuerySet, slice]):
    def __init__(self):
        super().__init__(translator=django_limit_offset_translator, executor=django_pagination_executor)


class QuerySetPageNumberPaginator(PageNumberPaginator[QuerySet, QuerySet, slice]):
    def __init__(self):
        super().__init__(translator=django_page_number_translator, executor=django_pagination_executor)
