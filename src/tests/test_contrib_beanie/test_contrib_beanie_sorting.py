import pytest

from fast_seeker.contrib.beanie.sorting import BeanieSorter, beanie_sorting_executor, beanie_sorting_translator

from .utils import DummyFindMany


@pytest.mark.parametrize(
    "order_by, expected",
    [
        (["-key1"], [("key1", -1)]),
        (["+key1"], [("key1", 1)]),
        (["key1"], [("key1", 1)]),
    ],
)
def test_beanie_sorting_translator(expected, sorting_query):
    translated_query = beanie_sorting_translator(sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        ([("key1", -1)], [("key1", -1)]),
        ([("key1", 1)], [("key1", 1)]),
    ],
)
def test_beanie_sorting_executor(translated_order, expected_expressions):
    result = beanie_sorting_executor(DummyFindMany(), translated_order)
    assert result.sort_expressions == expected_expressions


def test_beanie_sorter_ctor__should_properly_init_sorter():
    sorter = BeanieSorter()
    assert sorter.translator is not None
    assert sorter.executor is not None
