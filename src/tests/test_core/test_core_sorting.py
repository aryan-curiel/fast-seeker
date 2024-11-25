import pytest

from fast_seeker.core.sorting import OrderDirection, Sorter, SortingModel, parse_order_argument

#######################################################
# Tests for the default parse_order_argument function #
#######################################################


@pytest.mark.parametrize(
    "key_input,expected_key,expected_direction",
    [("key", "key", OrderDirection.ASC), ("-key", "key", OrderDirection.DESC), ("+key", "key", OrderDirection.ASC)],
)
def test_parse_order_argument(key_input, expected_key, expected_direction):
    key, direction = parse_order_argument(key_input)
    assert key == expected_key
    assert direction == expected_direction


##############################
# Tests for the Sorter class #
##############################


class FakeSorter(Sorter):
    def _apply_order(self, data, order):
        data.sorted_by = order
        return data


def test_sorter_parse_query():
    sorter = FakeSorter()
    sorting_model = SortingModel(order_by=["-key1", "+key2", "key3"])
    parsed_query = sorter._parse_query(sorting_model)
    assert parsed_query == [("key1", OrderDirection.DESC), ("key2", OrderDirection.ASC), ("key3", OrderDirection.ASC)]


def test_sorter_sort(monkeypatch):
    sorter = FakeSorter()
    data = type("Data", (), {"sorted_by": None})()
    sorting_model = SortingModel(order_by=["-key1", "+key2", "key3"])
    result = sorter.sort(data, sorting_model)
    assert result.sorted_by == [
        ("key1", OrderDirection.DESC),
        ("key2", OrderDirection.ASC),
        ("key3", OrderDirection.ASC),
    ]
