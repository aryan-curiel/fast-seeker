from fast_seeker.contrib.pymongo.sorting import ODManticSorter
from fast_seeker.core.sorting import SortingModel


def test_pymongo_sorter_sort__should_sort_data(pymongo_cursor):
    sorter = ODManticSorter()
    sort_query = SortingModel(order_by=["-field1", "+field2", "field3"])
    sorter.sort(pymongo_cursor, sort_query)
    pymongo_cursor.sort.assert_called_once_with([("field1", -1), ("field2", 1), ("field3", 1)])
