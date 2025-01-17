import pytest

from fast_seeker.contrib.pymongo.sorting import PyMongoSorter, pymongo_sorting_executor, pymongo_sorting_translator


@pytest.mark.parametrize(
    "order_by, expected",
    [
        (["-key1"], [("key1", -1)]),
        (["+key1"], [("key1", 1)]),
        (["key1"], [("key1", 1)]),
    ],
)
def test_pymongo_sorting_translator(expected, sorting_query):
    translated_query = pymongo_sorting_translator(sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        ([("key1", -1)], [("key1", -1)]),
        ([("key1", 1)], [("key1", 1)]),
    ],
)
def test_pymongo_sorting_executor(translated_order, expected_expressions, pymongo_cursor):
    cursor = pymongo_sorting_executor(pymongo_cursor, translated_order)
    cursor.sort.assert_called_once_with(expected_expressions)


def test_pymongo_sorter_ctor__should_properly_init_sorter():
    sorter = PyMongoSorter()
    assert sorter.translator is not None
    assert sorter.executor is not None
