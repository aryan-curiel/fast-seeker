from fast_seeker.contrib.odmantic.pagination import ODManticLimitOffsetTranslator, ODManticPageNumberTranslator
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery


def test_odmantic_limit_offset_translator__should_return_same_query():
    query = LimitOffsetQuery(limit=1, offset=2)
    result = ODManticLimitOffsetTranslator(query)
    assert result == query


def test_odmantic_page_number_translator__should_return_limit_offset_query():
    query = PageNumberQuery(page=1, size=2)
    result = ODManticPageNumberTranslator(query)
    assert result.limit == query.size
    assert result.offset == (query.page - 1) * query.size
