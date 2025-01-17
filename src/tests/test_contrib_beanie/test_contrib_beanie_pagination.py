import pytest

from fast_seeker.contrib.beanie.pagination import (
    BeanieLimitOffsetPaginator,
    BeaniePageNumberPaginator,
    beanie_limit_offset_translator,
    beanie_page_number_translator,
    beanie_pagination_executor,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery

from .utils import DummyFindMany


def test_beanie_limit_offset_translator__should_return_same_query():
    query = LimitOffsetQuery(limit=1, offset=2)
    result = beanie_limit_offset_translator(query)
    assert result == query


def test_beanie_page_number_translator__should_return_limit_offset_query():
    query = PageNumberQuery(page=1, size=2)
    result = beanie_page_number_translator(query)
    assert result.limit == query.size
    assert result.offset == (query.page - 1) * query.size


def test_beanie_pagination_executor__should_return_data_with_limit_and_offset():
    data = DummyFindMany()
    query = LimitOffsetQuery(limit=1, offset=2)
    result = beanie_pagination_executor(data, query)
    assert result.limit_number == query.limit
    assert result.skip_number == query.offset


@pytest.mark.parametrize(
    "paginator_class",
    [BeanieLimitOffsetPaginator, BeaniePageNumberPaginator],
)
def test_beanie_paginator__should_have_correct_translator_and_executor(paginator_class):
    paginator = paginator_class()
    assert paginator.translator is not None
    assert paginator.executor is not None
