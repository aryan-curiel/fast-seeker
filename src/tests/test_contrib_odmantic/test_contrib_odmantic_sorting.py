import pytest

from fast_seeker.contrib.odmantic.sorting import ODManticSorter
from fast_seeker.core.sorting import SortingModel

from .utils import DummyDocument


def test_odmantic_sorter_sort__should_sort_data():
    sorter = ODManticSorter()
    sort_query = SortingModel(order_by=["-field1", "+field2", "field3"])
    result = sorter.sort(DummyDocument, sort_query)
    assert result == (
        {"field1": -1},
        {"field2": 1},
        {"field3": 1},
    )


def test_odmantic_sorter_sort__raises_value_error_when_field_does_not_exist():
    sorter = ODManticSorter()
    sort_query = SortingModel(order_by=["-field1", "+field2", "field4"])
    with pytest.raises(ValueError):
        sorter.sort(DummyDocument, sort_query)
