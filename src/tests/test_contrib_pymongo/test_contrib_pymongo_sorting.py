import pytest

from fast_seeker.contrib.pymongo.sorting import PyMongoSorter


@pytest.mark.parametrize(
    "order_by, expected",
    [
        (["-key1"], [("key1", -1)]),
        (["+key1"], [("key1", 1)]),
        (["key1"], [("key1", 1)]),
    ],
)
def test_pymongo_sorter_translate(expected, sorting_query):
    translated_query = PyMongoSorter().translate(sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        ([("key1", -1)], [("key1", -1)]),
        ([("key1", 1)], [("key1", 1)]),
    ],
)
def test_pymongo_sorter_execute(translated_order, expected_expressions, pymongo_cursor):
    cursor = PyMongoSorter().execute(pymongo_cursor, translated_order)
    cursor.sort.assert_called_once_with(expected_expressions)


def test_pymongo_sorter_ctor__should_properly_init_sorter():
    sorter = PyMongoSorter()
    assert sorter.translator is not None
    assert sorter.executor is not None
