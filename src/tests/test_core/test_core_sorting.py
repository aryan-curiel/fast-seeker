import pytest

from fast_seeker.core.sorting import OrderEntry, SortDirection, Sorter, SortingModel

##########################
## Tests for OrderEntry ##
##########################


def test_order_entry_asc__should_return_order_entry_with_asc_direction():
    entry = OrderEntry.asc("key")
    assert entry.key == "key"
    assert entry.direction == SortDirection.ASC


def test_order_entry_desc__should_return_order_entry_with_desc_direction():
    entry = OrderEntry.desc("key")
    assert entry.key == "key"
    assert entry.direction == SortDirection.DESC


################################
## Tests for the SortingModel ##
################################


@pytest.mark.parametrize(
    "key_input,expected_entry",
    [("key", OrderEntry.asc("key")), ("-key", OrderEntry.desc("key")), ("+key", OrderEntry.asc("key"))],
)
def test_sorting_model_parse_entry__should_return_expected_entry_when_valid_value(key_input, expected_entry):
    entry = SortingModel._parse_entry(key_input)
    assert entry == expected_entry


def test_sorting_model_parsed__should_return_expected_entries():
    sorting_model = SortingModel(order_by=["-key1", "+key2", "key3"])
    parsed = list(sorting_model.parsed)
    assert parsed == [OrderEntry.desc("key1"), OrderEntry.asc("key2"), OrderEntry.asc("key3")]


##############################
# Tests for the Sorter class #
##############################


class FakeSorter(Sorter):
    def get_order(self, sort_query):
        return sort_query.order_by

    def _apply_order(self, data, order):
        data.sorted_by = order
        return data


class Data:
    def __init__(self):
        self.sorted_by = None


def test_sorter_sort__applies_sort_when_query_provided():
    sorter = FakeSorter()
    order_args = ["-key1", "+key2", "key3"]
    sorting_model = SortingModel(order_by=order_args)
    result = sorter.sort(Data(), sorting_model)
    assert result.sorted_by == order_args


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


def test_sorter__raises_not_implemented_error_when_abstract_not_implemented():
    class DummySorter(Sorter):
        def get_order(self, sort_query):
            return super().get_order(sort_query)

        def _apply_order(self, data, order: list[tuple[str, SortDirection]]):
            return super()._apply_order(data, order)

    with pytest.raises(NotImplementedError):
        DummySorter()._apply_order(None, None)

    with pytest.raises(NotImplementedError):
        DummySorter().get_order(None)
