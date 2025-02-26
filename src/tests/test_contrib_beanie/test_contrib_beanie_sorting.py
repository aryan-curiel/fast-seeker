import pytest

from fast_seeker.contrib.beanie.sorting import BeanieSorter, BeanieSortingQueryExecutor, BeanieSortingQueryTranslator
from fast_seeker.core.sorting import SortingQuery

from .utils import DummyFindMany


@pytest.mark.parametrize(
    "sorting_query, expected",
    [
        pytest.param(SortingQuery(order_by=["-field1"]), [("field1", -1)], id="descending"),
        pytest.param(SortingQuery(order_by=["+field1"]), [("field1", 1)], id="ascending_explicit"),
        pytest.param(SortingQuery(order_by=["field1"]), [("field1", 1)], id="ascending"),
    ],
)
def test_beanie_sorter_translator(sorting_query, expected):
    translator = BeanieSortingQueryTranslator()
    translated_query = list(translator.translate(query=sorting_query))
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        pytest.param([("field1", -1)], [("field1", -1)], id="descending"),
        pytest.param([("field1", 1)], [("field1", 1)], id="ascending"),
    ],
)
def test_beanie_sorter_executor(translated_order, expected_expressions):
    executor = BeanieSortingQueryExecutor()
    result = executor.execute(source=DummyFindMany(), translated_query=translated_order)
    assert result.sort_expressions == expected_expressions


def test_beanie_sorter__should_have_correct_translator_and_executor():
    sorter = BeanieSorter()
    assert isinstance(sorter.translator, BeanieSortingQueryTranslator)
    assert isinstance(sorter.executor, BeanieSortingQueryExecutor)
