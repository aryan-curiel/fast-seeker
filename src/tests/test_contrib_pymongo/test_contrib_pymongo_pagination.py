import pytest

from fast_seeker.contrib.pymongo.pagination import (
    PyMongoLimitOffsetPaginator,
    PyMongoPageNumberPaginator,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery


@pytest.mark.parametrize(
    "paginator_class, query, expected_limit, expected_offset",
    [
        pytest.param(PyMongoLimitOffsetPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="limit_offset"),
        pytest.param(PyMongoPageNumberPaginator, PageNumberQuery(page=1, size=2), 2, 0, id="page_number"),
    ],
)
def test_pymongo_paginator_translate__should_return_correct_query(
    paginator_class, query, expected_limit, expected_offset, pymongo_cursor
):
    paginator = paginator_class()
    result = paginator.translate(pymongo_cursor, query)
    assert result.limit == expected_limit
    assert result.offset == expected_offset


@pytest.mark.parametrize(
    "paginator_class, query, expected_limit, expected_offset",
    [
        pytest.param(PyMongoLimitOffsetPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="limit_offset"),
        pytest.param(PyMongoPageNumberPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="page_number"),
    ],
)
def test_pymongo_paginator_execute__should_return_data_with_limit_and_offset(
    paginator_class, query, expected_limit, expected_offset, pymongo_cursor
):
    paginator_class().execute(pymongo_cursor, query)
    pymongo_cursor.limit.assert_called_once_with(expected_limit)
    pymongo_cursor.skip.assert_called_once_with(expected_offset)
