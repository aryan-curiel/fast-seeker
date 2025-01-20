import pytest

from fast_seeker.contrib.odmantic.engines import ODManticFindQueryBuilder
from fast_seeker.contrib.odmantic.sorting import ODManticSorter
from fast_seeker.core.sorting import SortingQuery

from .utils import DummyDocument


@pytest.mark.parametrize(
    "sorting_query, expected",
    [
        (SortingQuery(order_by=["-field1"]), ({"field1": -1},)),
        (SortingQuery(order_by=["+field1"]), ({"field1": 1},)),
        (SortingQuery(order_by=["field1"]), ({"field1": 1},)),
    ],
)
def test_odmantic_sorter_translate(sorting_query, expected, mocker):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    translated_query = ODManticSorter().translate(query_builder, sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        (({"field1": -1},), ({"field1": -1},)),
        (({"field1": 1},), ({"field1": 1},)),
    ],
)
def test_odmantic_sorter_execute(translated_order, expected_expressions, mocker):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    returned_query_builder = ODManticSorter().execute(query_builder, translated_order)
    assert returned_query_builder == query_builder
    assert returned_query_builder._sort == expected_expressions
