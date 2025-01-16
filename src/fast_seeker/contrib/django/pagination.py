from django.db.models import QuerySet

from fast_seeker.core.pagination.limit_offset import LimitOffsetModel, LimitOffsetPaginator
from fast_seeker.core.pagination.page_number import PageNumberModel, PageNumberPaginator


class QuerySetLimitOffsetPaginator(LimitOffsetPaginator[QuerySet, QuerySet]):
    def paginate(self, data: QuerySet, page_query: LimitOffsetModel) -> QuerySet:
        return data[page_query.offset : page_query.offset + page_query.limit]


class QuerySetPageNumberPaginator(PageNumberPaginator[QuerySet, QuerySet]):
    def paginate(self, data: QuerySet, page_query: PageNumberModel) -> QuerySet:
        return data[(page_query.page - 1) * page_query.size : page_query.page * page_query.size]
