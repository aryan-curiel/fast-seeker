import pytest

from fast_seeker.contrib.beanie.pagination import (
    BeanieLimitOffsetPaginator,
    BeanieLimitOffsetQueryTranslator,
    BeaniePageNumberPaginator,
    BeaniePageNumberQueryTranslator,
    BeaniePaginationExecutor,
    BeanieQueryPage,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery

from .utils import DummyFindMany


@pytest.mark.parametrize(
    "translator_class, query, expected_translation",
    [
        pytest.param(
            BeanieLimitOffsetQueryTranslator,
            LimitOffsetQuery(limit=1, offset=2),
            BeanieQueryPage(limit=1, skip=2),
            id="limit_offset",
        ),
        pytest.param(
            BeaniePageNumberQueryTranslator,
            PageNumberQuery(page=1, size=2),
            BeanieQueryPage(limit=2, skip=0),
            id="page_number",
        ),
    ],
)
def test_beanie_pagination_translators(translator_class, query, expected_translation):
    translator = translator_class()
    result = translator.translate(query=query)
    assert result == expected_translation


def test_beanie_pagination_executor__should_return_data_with_limit_and_offset():
    executor = BeaniePaginationExecutor()
    translated_query = BeanieQueryPage(limit=1, skip=2)
    result = executor.execute(source=DummyFindMany(), translated_query=translated_query)
    assert result.limit_number == translated_query["limit"]
    assert result.skip_number == translated_query["skip"]


def test_beanie_limit_offset_paginator__should_have_correct_translator_and_executor():
    paginator = BeanieLimitOffsetPaginator()
    assert isinstance(paginator.translator, BeanieLimitOffsetQueryTranslator)
    assert isinstance(paginator.executor, BeaniePaginationExecutor)


def test_beanie_page_number_paginator__should_have_correct_translator_and_executor():
    paginator = BeaniePageNumberPaginator()
    assert isinstance(paginator.translator, BeaniePageNumberQueryTranslator)
    assert isinstance(paginator.executor, BeaniePaginationExecutor)
