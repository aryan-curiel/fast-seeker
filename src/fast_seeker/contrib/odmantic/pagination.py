from typing import Any, TypedDict

from fast_seeker.core.pagination.limit_offset import LimitOffsetModel, LimitOffsetPaginator
from fast_seeker.core.pagination.page_number import PageNumberModel, PageNumberPaginator


class ODManticPaginationArgs(TypedDict):
    skip: int = 0
    limit: int | None = None


class ODManticLimitOffsetPaginator(LimitOffsetPaginator[Any, ODManticPaginationArgs]):
    def paginate(self, page_query: LimitOffsetModel) -> ODManticPaginationArgs:
        return ODManticPaginationArgs(skip=page_query.offset, limit=page_query.limit)


class ODManticPageNumberPaginator(PageNumberPaginator[Any, ODManticPaginationArgs]):
    def paginate(self, page_query: PageNumberModel) -> ODManticPaginationArgs:
        return ODManticPaginationArgs(skip=(page_query.page - 1) * page_query.size, limit=page_query.size)
