import pytest

from fast_seeker.contrib.pymongo.pagination import (
    PyMongoLimitOffsetPaginator,
    PyMongoPageNumberPaginator,
    pymongo_limit_offset_translator,
    pymongo_page_number_translator,
    pymongo_pagination_executor,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery


def test_pymongo_limit_offset_translator__should_return_same_query():
    query = LimitOffsetQuery(limit=1, offset=2)
    result = pymongo_limit_offset_translator(query)
    assert result == query


def test_pymongo_page_number_translator__should_return_limit_offset_query():
    query = PageNumberQuery(page=1, size=2)
    result = pymongo_page_number_translator(query)
    assert result.limit == query.size
    assert result.offset == (query.page - 1) * query.size


def test_pymongo_pagination_executor__should_return_data_with_limit_and_offset(pymongo_cursor):
    query = LimitOffsetQuery(limit=1, offset=2)
    pymongo_pagination_executor(pymongo_cursor, query)
    pymongo_cursor.limit.assert_called_once_with(query.limit)
    pymongo_cursor.skip.assert_called_once_with(query.offset)


@pytest.mark.parametrize(
    "paginator_class",
    [PyMongoLimitOffsetPaginator, PyMongoPageNumberPaginator],
)
def test_pymongo_paginator__should_have_correct_translator_and_executor(paginator_class):
    paginator = paginator_class()
    assert paginator.translator is not None
    assert paginator.executor is not None
