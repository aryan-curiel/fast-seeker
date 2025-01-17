from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery


def ODManticLimitOffsetTranslator(query: LimitOffsetQuery) -> LimitOffsetQuery:
    return query


def ODManticPageNumberTranslator(query: PageNumberQuery) -> LimitOffsetQuery:
    return LimitOffsetQuery(limit=query.size, offset=(query.page - 1) * query.size)
