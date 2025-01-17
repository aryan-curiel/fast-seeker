import pytest
from django.db.models import QuerySet

from fast_seeker.contrib.django.pagination import (
    QuerySetLimitOffsetPaginator,
    QuerySetPageNumberPaginator,
    django_limit_offset_translator,
    django_page_number_translator,
    django_pagination_executor,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery


def test_django_limit_offset_translator__should_return_slice():
    query = LimitOffsetQuery(limit=1, offset=2)
    result = django_limit_offset_translator(query)
    assert result == slice(2, 3)


def test_django_page_number_translator__should_return_slice():
    query = PageNumberQuery(page=1, size=2)
    result = django_page_number_translator(query)
    assert result == slice(0, 2)


def test_django_pagination_executor__should_return_data_with_slice(mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)
    query = slice(1, 3)
    django_pagination_executor(mock_queryset, query)
    mock_queryset.__getitem__.assert_called_once_with(query)


@pytest.mark.parametrize(
    "paginator_class",
    [QuerySetLimitOffsetPaginator, QuerySetPageNumberPaginator],
)
def test_queryset_paginator__should_have_correct_translator_and_executor(paginator_class):
    paginator = paginator_class()
    assert paginator.translator is not None
    assert paginator.executor is not None
