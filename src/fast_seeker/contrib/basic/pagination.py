from collections.abc import Sequence

from fast_seeker.core.pagination import LimitOffsetPaginator, PageNumberPaginator


class BasicLimitOffsetPaginator(LimitOffsetPaginator[Sequence, Sequence]):
    def paginate(self, data: Sequence, page_query: Sequence) -> Sequence:
        from_index = page_query.offset
        to_index = page_query.offset + page_query.limit
        return data[from_index:to_index]


class BasicPageNumberPaginator(PageNumberPaginator[Sequence, Sequence]):
    def paginate(self, data: Sequence, page_query: Sequence) -> Sequence:
        from_index = page_query.page * page_query.page_size
        to_index = from_index + page_query.page_size
        return data[from_index:to_index]
