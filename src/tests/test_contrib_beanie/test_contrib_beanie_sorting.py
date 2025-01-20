import pytest

from fast_seeker.contrib.beanie.sorting import BeanieSorter
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
def test_beanie_sorter_translate(sorting_query, expected):
    translated_query = BeanieSorter().translate(DummyFindMany(), sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        pytest.param([("field1", -1)], [("field1", -1)], id="descending"),
        pytest.param([("field1", 1)], [("field1", 1)], id="ascending"),
    ],
)
def test_beanie_sorter_execute(translated_order, expected_expressions):
    result = BeanieSorter().execute(DummyFindMany(), translated_order)
    assert result.sort_expressions == expected_expressions
