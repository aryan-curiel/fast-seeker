from django.db.models import QuerySet

from fast_seeker.core.pagination import LimitOffsetPaginator, LimitOffsetQuery, PageNumberPaginator, PageNumberQuery


class QuerySetLimitOffsetPaginator(LimitOffsetPaginator[QuerySet, QuerySet, slice]):
    def translate(self, query: LimitOffsetQuery) -> slice:
        return slice(query.offset, query.offset + query.limit)

    def execute(self, data: QuerySet, args: slice) -> QuerySet:
        return data[args]


class QuerySetPageNumberPaginator(PageNumberPaginator[QuerySet, QuerySet, slice]):
    def translate(self, query: PageNumberQuery) -> slice:
        return slice((query.page - 1) * query.size, query.page * query.size)

    def execute(self, data: QuerySet, args: slice) -> QuerySet:
        return data[args]
