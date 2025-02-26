import pytest
from django.db.models import QuerySet

from fast_seeker.contrib.django.sorting import DjangoSorter, DjangoSortingQueryExecutor, DjangoSortingQueryTranslator
from fast_seeker.core.sorting import SortingQuery


@pytest.mark.parametrize(
    "sorting_query, expected",
    [
        pytest.param(SortingQuery(order_by=["-field1"]), ["-field1"], id="descending"),
        pytest.param(SortingQuery(order_by=["+field1"]), ["field1"], id="ascending_explicit"),
        pytest.param(SortingQuery(order_by=["field1"]), ["field1"], id="ascending"),
    ],
)
def test_django_sorting_translator(sorting_query, expected, mocker):
    translator = DjangoSortingQueryTranslator()
    translated_query = list(translator.translate(query=sorting_query))
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order",
    [
        pytest.param(["field1"], id="descending"),
        pytest.param(["-field1"], id="ascending"),
    ],
)
def test_django_sorting_executor(translated_order, mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)
    executor = DjangoSortingQueryExecutor()

    executor.execute(source=mock_queryset, translated_query=translated_order)
    mock_queryset.order_by.assert_called_once_with(*translated_order)


def test_django_sorter__should_have_correct_translator_and_executor():
    sorter = DjangoSorter()
    assert isinstance(sorter.translator, DjangoSortingQueryTranslator)
    assert isinstance(sorter.executor, DjangoSortingQueryExecutor)
