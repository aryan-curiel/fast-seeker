from fast_seeker.contrib.pymongo.sorting import PyMongoSorter
from fast_seeker.core.sorting import SortingModel

#######################################
## Tests for the PyMongoSorter class ##
#######################################


def test_pymongo_sorter_get_order__should_return_expected_order():
    sort_query = SortingModel(order_by=["-key1", "+key2", "key3"])
    order = PyMongoSorter().get_order(sort_query)
    assert order == [
        ("key1", -1),
        ("key2", 1),
        ("key3", 1),
    ]


def test_pymongo_sorter_apply_sort__should_apply_sorting_in_beanie(pymongo_cursor):
    sort_query = [
        ("key1", -1),
        ("key2", 1),
        ("key3", 1),
    ]
    PyMongoSorter()._apply_order(pymongo_cursor, sort_query)
    pymongo_cursor.sort.assert_called_once_with(sort_query)
