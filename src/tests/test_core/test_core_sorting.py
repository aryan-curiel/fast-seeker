import pytest

from fast_seeker.core.sorting import OrderEntry, SortDirection, SortingQuery

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
    entry = SortingQuery._parse_entry(key_input)
    assert entry == expected_entry


def test_sorting_model_parsed__should_return_expected_entries():
    sorting_model = SortingQuery(order_by=["-key1", "+key2", "key3"])
    parsed = list(sorting_model.parsed)
    assert parsed == [OrderEntry.desc("key1"), OrderEntry.asc("key2"), OrderEntry.asc("key3")]
