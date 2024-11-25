import pytest

from fast_seeker.core.sorting import OrderEntry, SortDirection, SortingQuery, SortingQueryBaseTranslator

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


##############################################
## Tests for the SortingQueryBaseTranslator ##
##############################################


class DummySortingQueryTranslator(SortingQueryBaseTranslator):
    def __call__(self, *, query, **kwargs):
        return self._translate_as_entries(query)


@pytest.mark.parametrize(
    "key_input,expected_entry",
    [
        pytest.param("key", OrderEntry.asc("key"), id="ascending"),
        pytest.param("-key", OrderEntry.desc("key"), id="descending"),
        pytest.param("+key", OrderEntry.asc("key"), id="explicit_ascending"),
    ],
)
def test_sorting_query_base_translator_parse_entry__returns_expected_entry_when_valid_value(key_input, expected_entry):
    entry = DummySortingQueryTranslator._parse_entry(key_input)
    assert entry == expected_entry


class ClassLevelOnlySortingQueryTranslator(DummySortingQueryTranslator):
    def translate_key(self, query, entry):
        return OrderEntry.asc("translated_key")


class ConfigOnlyStringSortingQueryTranslator(DummySortingQueryTranslator):
    config = {"field_translators": {"key": "translated_key"}}


class ConfigOnlyCallableSortingQueryTranslator(DummySortingQueryTranslator):
    config = {"field_translators": {"key": lambda query, entry: OrderEntry.asc("translated_key")}}


class ConfigAndClassLevelSortingQueryTranslator(DummySortingQueryTranslator):
    config = {"field_translators": {"key": "config_translated_key"}}

    def translate_key(self, query, entry):
        return OrderEntry.asc("translated_key")


@pytest.mark.parametrize(
    "entry,translator,expected_result",
    [
        pytest.param(
            OrderEntry.asc("key"), DummySortingQueryTranslator(), OrderEntry.asc("key"), id="with_no_translation"
        ),
        pytest.param(
            OrderEntry.asc("key"),
            ClassLevelOnlySortingQueryTranslator(),
            OrderEntry.asc("translated_key"),
            id="with_class_level_translation",
        ),
        pytest.param(
            OrderEntry.asc("key"),
            ConfigOnlyStringSortingQueryTranslator(),
            OrderEntry.asc("translated_key"),
            id="with_config_level_string_translation",
        ),
        pytest.param(
            OrderEntry.asc("key"),
            ConfigOnlyCallableSortingQueryTranslator(),
            OrderEntry.asc("translated_key"),
            id="with_config_level_callable_translation",
        ),
        pytest.param(
            OrderEntry.asc("key"),
            ConfigAndClassLevelSortingQueryTranslator(),
            OrderEntry.asc("translated_key"),
            id="with_config_and_class_level_translation",
        ),
    ],
)
def test_sorting_query_base_translator_translate_entry(entry, translator, expected_result):
    result = translator._translate_entry(None, entry)
    assert result == expected_result


def test_sorting_query_base_translator_translate_entry__raises_value_error_when_invalid_translator_provided():
    class InvalidTranslator(DummySortingQueryTranslator):
        config = {"field_translators": {"key": 123}}

    translator = InvalidTranslator()
    query = SortingQuery(order_by=["key"])

    entry = OrderEntry.asc("key")
    with pytest.raises(ValueError):
        translator._translate_entry(query, entry)


def test_sorting_query_translate__returns_expected_entries():
    translator = DummySortingQueryTranslator()
    query = SortingQuery(order_by=["key1", "-key2", "+key3"])

    result = translator(query=query)
    assert list(result) == [
        OrderEntry.asc("key1"),
        OrderEntry.desc("key2"),
        OrderEntry.asc("key3"),
    ]
