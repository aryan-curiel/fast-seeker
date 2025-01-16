from fast_seeker.contrib.beanie.sorting import BeanieSorter
from fast_seeker.core.sorting import SortingModel

from .utils import DummyFindMany

######################################
## Tests for the BeanieSorter class ##
######################################


def test_beanie_sorter_get_order__should_return_expected_order():
    sort_query = SortingModel(order_by=["-key1", "+key2", "key3"])
    order = BeanieSorter().get_order(sort_query)
    assert order == [
        ("key1", -1),
        ("key2", 1),
        ("key3", 1),
    ]


def test_beanie_sorter_apply_sort__should_apply_sorting_in_beanie():
    data = DummyFindMany()
    sort_query = [
        ("key1", -1),
        ("key2", 1),
        ("key3", 1),
    ]
    result = BeanieSorter()._apply_order(data, sort_query)
    assert result.sort_expressions == [
        ("key1", -1),
        ("key2", 1),
        ("key3", 1),
    ]
