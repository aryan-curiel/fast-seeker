import pytest

from fast_seeker.contrib.odmantic.engines import ODManticFindQueryBuilder
from fast_seeker.contrib.odmantic.pagination import (
    ODManticLimitOffsetPaginator,
    ODManticPageNumberPaginator,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery

from .utils import DummyDocument


@pytest.mark.parametrize(
    "paginator_class, query, expected_limit, expected_offset",
    [
        pytest.param(ODManticLimitOffsetPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="limit_offset"),
        pytest.param(ODManticPageNumberPaginator, PageNumberQuery(page=1, size=2), 2, 0, id="page_number"),
    ],
)
def test_pymongo_paginator_translate__should_return_correct_query(
    paginator_class, query, expected_limit, expected_offset, mocker
):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    translated_query = paginator_class().translate(query_builder, query)
    assert translated_query.limit == expected_limit
    assert translated_query.offset == expected_offset


@pytest.mark.parametrize(
    "paginator_class, query, expected_limit, expected_offset",
    [
        pytest.param(ODManticLimitOffsetPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="limit_offset"),
        pytest.param(ODManticPageNumberPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="page_number"),
    ],
)
def test_pymongo_paginator_execute__should_return_data_with_limit_and_offset(
    paginator_class, query, expected_limit, expected_offset, mocker
):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    returned_query_builder = paginator_class().execute(query_builder, query)
    assert returned_query_builder._limit == expected_limit
    assert returned_query_builder._skip == expected_offset
