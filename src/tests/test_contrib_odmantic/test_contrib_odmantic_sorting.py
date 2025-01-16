from fast_seeker.contrib.odmantic.sorting import ODManticOrderBuilder
from fast_seeker.core.sorting import SortingModel

from .utils import DummyDocument


def test_pymongo_sorter_get_order__should_return_expected_order():
    sort_query = SortingModel(order_by=["-field1", "+field2", "field3"])
    order = ODManticOrderBuilder().get_order(DummyDocument, sort_query)
    assert order == (
        {"field1": -1},
        {"field2": 1},
        {"field3": 1},
    )
