import pytest
from django.db.models import QuerySet

from fast_seeker.contrib.django.sorting import QuerySetSorter


@pytest.mark.parametrize(
    "order_by, expected",
    [
        (["-key1"], ["-key1"]),
        (["+key1"], ["+key1"]),
        (["key1"], ["key1"]),
    ],
)
def test_django_sorting_translate(expected, sorting_query):
    translated_query = QuerySetSorter().translate(sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        ([("key1", -1)], [("key1", -1)]),
        ([("key1", 1)], [("key1", 1)]),
    ],
)
def test_django_sorting_execute(translated_order, expected_expressions, mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)

    QuerySetSorter().execute(mock_queryset, translated_order)
    mock_queryset.order_by.assert_called_once_with(*expected_expressions)
