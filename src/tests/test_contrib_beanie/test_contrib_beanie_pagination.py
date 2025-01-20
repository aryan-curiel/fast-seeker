import pytest

from fast_seeker.contrib.beanie.pagination import (
    BeanieLimitOffsetPaginator,
    BeaniePageNumberPaginator,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery

from .utils import DummyFindMany


@pytest.mark.parametrize(
    "paginator_class, query, expected_limit, expected_offset",
    [
        pytest.param(BeanieLimitOffsetPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="limit_offset"),
        pytest.param(BeaniePageNumberPaginator, PageNumberQuery(page=1, size=2), 2, 0, id="page_number"),
    ],
)
def test_beanie_paginator_translate__should_return_correct_query(
    paginator_class, query, expected_limit, expected_offset
):
    result = paginator_class().translate(DummyFindMany(), query)
    assert result.limit == expected_limit
    assert result.offset == expected_offset


@pytest.mark.parametrize(
    "paginator_class, query, expected_limit, expected_offset",
    [
        pytest.param(BeanieLimitOffsetPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="limit_offset"),
        pytest.param(BeaniePageNumberPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="page_number"),
    ],
)
def test_beanie_paginator_executor__should_return_data_with_limit_and_offset(
    paginator_class, query, expected_limit, expected_offset
):
    data = DummyFindMany()
    result = paginator_class().execute(data, query)
    assert result.limit_number == expected_limit
    assert result.skip_number == expected_offset
