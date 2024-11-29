from beanie.odm.queries.find import FindMany

from fast_seeker.core.pagination.limit_offset import LimitOffsetModel, LimitOffsetPaginator
from fast_seeker.core.pagination.page_number import PageNumberModel, PageNumberPaginator


class BeanieLimitOffsetPaginator(LimitOffsetPaginator[FindMany, FindMany]):
    def paginate(self, data: FindMany, page_query: LimitOffsetModel) -> FindMany:
        return data.limit(page_query.limit).skip(page_query.offset)


class BeaniePageNumberPaginator(PageNumberPaginator[FindMany, FindMany]):
    def paginate(self, data: FindMany, page_query: PageNumberModel) -> FindMany:
        return data.limit(page_query.size).skip((page_query.page - 1) * page_query.size)
