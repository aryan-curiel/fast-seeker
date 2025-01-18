import pytest

from fast_seeker.contrib.beanie.sorting import BeanieSorter

from .utils import DummyFindMany


@pytest.mark.parametrize(
    "order_by, expected",
    [
        (["-key1"], [("key1", -1)]),
        (["+key1"], [("key1", 1)]),
        (["key1"], [("key1", 1)]),
    ],
)
def test_beanie_sorter_translate(expected, sorting_query):
    translated_query = BeanieSorter().translate(DummyFindMany(), sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        ([("key1", -1)], [("key1", -1)]),
        ([("key1", 1)], [("key1", 1)]),
    ],
)
def test_beanie_sorter_execute(translated_order, expected_expressions):
    result = BeanieSorter().execute(DummyFindMany(), translated_order)
    assert result.sort_expressions == expected_expressions
