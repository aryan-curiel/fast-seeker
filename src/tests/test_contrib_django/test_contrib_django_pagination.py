import pytest
from django.db.models import QuerySet

from fast_seeker.contrib.django.pagination import (
    QuerySetLimitOffsetPaginator,
    QuerySetPageNumberPaginator,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery


@pytest.mark.parametrize(
    "paginator_class, query, expected_slice",
    [
        (QuerySetLimitOffsetPaginator, LimitOffsetQuery(limit=1, offset=2), slice(2, 3)),
        (QuerySetPageNumberPaginator, PageNumberQuery(page=1, size=2), slice(0, 2)),
    ],
)
def test_django_paginator_translate__should_return_slice(paginator_class, query, expected_slice, mocker):
    paginator = paginator_class()
    result = paginator.translate(mocker.MagicMock(spec=QuerySet).query)
    assert result == expected_slice


@pytest.mark.parametrize(
    "paginator_class, query, expected_slice",
    [
        (QuerySetLimitOffsetPaginator, slice(2, 3), slice(2, 3)),
        (QuerySetPageNumberPaginator, slice(0, 2), slice(0, 2)),
    ],
)
def test_django_paginator_executor__should_return_data_with_slice(paginator_class, query, expected_slice, mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)
    paginator = paginator_class()
    paginator.execute(mock_queryset, query)
    mock_queryset.__getitem__.assert_called_once_with(expected_slice)
