import pytest
from django.db.models import QuerySet

from fast_seeker.contrib.django.sorting import QuerySetSorter
from fast_seeker.core.sorting import SortingQuery


@pytest.mark.parametrize(
    "sorting_query, expected",
    [
        pytest.param(SortingQuery(order_by=["-field1"]), ["-field1"], id="descending"),
        pytest.param(SortingQuery(order_by=["+field1"]), ["+field1"], id="ascending_explicit"),
        pytest.param(SortingQuery(order_by=["field1"]), ["field1"], id="ascending"),
    ],
)
def test_django_sorting_translate(sorting_query, expected, mocker):
    translated_query = QuerySetSorter().translate(mocker.MagicMock(spec=QuerySet), sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        pytest.param([("field1", -1)], [("field1", -1)], id="descending"),
        pytest.param([("field1", 1)], [("field1", 1)], id="ascending"),
    ],
)
def test_django_sorting_execute(translated_order, expected_expressions, mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)

    QuerySetSorter().execute(mock_queryset, translated_order)
    mock_queryset.order_by.assert_called_once_with(*expected_expressions)
