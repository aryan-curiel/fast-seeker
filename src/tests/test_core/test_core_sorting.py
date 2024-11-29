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


class Data:
    def __init__(self):
        self.sorted_by = None


def test_sorter_parse_query():
    sorter = FakeSorter()
    sorting_model = SortingModel(order_by=["-key1", "+key2", "key3"])
    parsed_query = sorter._parse_query(sorting_model)
    assert parsed_query == [("key1", OrderDirection.DESC), ("key2", OrderDirection.ASC), ("key3", OrderDirection.ASC)]


def test_sorter_sort__applies_sort_when_query_provided():
    sorter = FakeSorter()
    sorting_model = SortingModel(order_by=["-key1", "+key2", "key3"])
    result = sorter.sort(Data(), sorting_model)
    assert result.sorted_by == [
        ("key1", OrderDirection.DESC),
        ("key2", OrderDirection.ASC),
        ("key3", OrderDirection.ASC),
    ]


def test_sorter_sort__returns_data_when_no_query_provided():
    sorter = FakeSorter()
    sorting_model = SortingModel(order_by=[])
    result = sorter.sort(Data(), sorting_model)
    assert result.sorted_by is None


def test_sorter__raises_type_error_when_not_implemented():
    class DummySorter(Sorter):
        pass

    with pytest.raises(TypeError):
        DummySorter()


def test_sorter__raises_not_implemented_error_when_apply_order_not_implemented():
    class DummySorter(Sorter):
        def _apply_order(self, data, order: list[tuple[str, OrderDirection]]):
            return super()._apply_order(data, order)

    with pytest.raises(NotImplementedError):
        DummySorter()._apply_order(None, None)
