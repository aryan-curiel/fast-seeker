import pytest
from django.db.models import QuerySet

from fast_seeker.contrib.django.pagination import (
    DjangoLimitOffsetPaginator,
    DjangoLimitOffsetQueryTranslator,
    DjangoPageNumberPaginator,
    DjangoPageNumberQueryTranslator,
    DjangoPaginationExecutor,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery


@pytest.mark.parametrize(
    "translator_class, query, expected_slice",
    [
        pytest.param(
            DjangoLimitOffsetQueryTranslator, LimitOffsetQuery(limit=1, offset=2), slice(2, 3), id="limit_offset"
        ),
        pytest.param(DjangoPageNumberQueryTranslator, PageNumberQuery(page=1, size=2), slice(0, 2), id="page_number"),
    ],
)
def test_django_pagination_translators(translator_class, query, expected_slice, mocker):
    translator = translator_class()
    result = translator.translate(query=query)
    assert result == expected_slice


def test_django_pagination_executor__should_apply_slice(mocker):
    executor = DjangoPaginationExecutor()
    mock_queryset = mocker.MagicMock(spec=QuerySet)
    translated_query_slice = slice(2, 3)
    executor.execute(source=mock_queryset, translated_query=translated_query_slice)
    mock_queryset.__getitem__.assert_called_once_with(translated_query_slice)


def test_django_limit_offset_paginator__should_have_correct_translator_and_executor():
    paginator = DjangoLimitOffsetPaginator()
    assert isinstance(paginator.translator, DjangoLimitOffsetQueryTranslator)
    assert isinstance(paginator.executor, DjangoPaginationExecutor)


def test_django_page_number_paginator__should_have_correct_translator_and_executor():
    paginator = DjangoPageNumberPaginator()
    assert isinstance(paginator.translator, DjangoPageNumberQueryTranslator)
    assert isinstance(paginator.executor, DjangoPaginationExecutor)
