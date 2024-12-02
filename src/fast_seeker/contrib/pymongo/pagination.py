from pymongo.cursor import Cursor

from fast_seeker.core.pagination.limit_offset import LimitOffsetModel, LimitOffsetPaginator
from fast_seeker.core.pagination.page_number import PageNumberModel, PageNumberPaginator


class PyMongoLimitOffsetPaginator(LimitOffsetPaginator[Cursor, Cursor]):
    def paginate(self, cursor: Cursor, page_query: LimitOffsetModel) -> Cursor:
        return cursor.skip(page_query.offset).limit(page_query.limit)


class PyMongoPageNumberPaginator(PageNumberPaginator[Cursor, Cursor]):
    def paginate(self, cursor: Cursor, page_query: PageNumberModel) -> Cursor:
        return cursor.skip((page_query.page - 1) * page_query.size).limit(page_query.size)
