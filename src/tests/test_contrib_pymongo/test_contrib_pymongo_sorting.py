import pytest

from fast_seeker.contrib.pymongo.sorting import PyMongoSorter
from fast_seeker.core.sorting import SortingQuery


@pytest.mark.parametrize(
    "sorting_query, expected",
    [
        (SortingQuery(order_by=["-field1"]), [("field1", -1)]),
        (SortingQuery(order_by=["+field1"]), [("field1", 1)]),
        (SortingQuery(order_by=["field1"]), [("field1", 1)]),
    ],
)
def test_pymongo_sorter_translate(sorting_query, expected, pymongo_cursor):
    translated_query = PyMongoSorter().translate(pymongo_cursor, sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        ([("field1", -1)], [("field1", -1)]),
        ([("field1", 1)], [("field1", 1)]),
    ],
)
def test_pymongo_sorter_execute(translated_order, expected_expressions, pymongo_cursor):
    cursor = PyMongoSorter().execute(pymongo_cursor, translated_order)
    cursor.sort.assert_called_once_with(expected_expressions)
