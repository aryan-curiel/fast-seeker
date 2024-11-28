from fast_seeker.contrib.beanie.sorting import BeanieSorter
from fast_seeker.core.sorting import SortingModel

from .utils import DummyFindMany


def test_beanie_sorter_sort__should_sort_data():
    sorter = BeanieSorter()
    data = DummyFindMany()
    sort_query = SortingModel(order_by=["-key1", "+key2", "key3"])
    result = sorter.sort(data, sort_query)
    assert result.sort_expressions == [
        ("key1", -1),
        ("key2", 1),
        ("key3", 1),
    ]
