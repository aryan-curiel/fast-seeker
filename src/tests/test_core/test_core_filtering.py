from typing import Any, Union

import pytest

from fast_seeker.core.filtering import FiltererConfigDict, FilterQuery, FilterQueryBaseTranslator


class DummyFilter(FilterQuery):
    field: Union[str, None] = None
    another_field: Union[str, None] = None


class DummyFilterQueryTranslator(FilterQueryBaseTranslator):
    def _default_field_translator(self, query, field_name, field_value) -> dict[str, Any]:
        return {field_name: field_value}


class DummyFilterQueryTranslatorWithCustomFieldTranslator(DummyFilterQueryTranslator):
    def translate_field(self, query, field_name, field_value) -> dict[str, Any]:
        return {field_name: "custom"}


class DummyFilterQueryTranslatorWithCustomFieldTranslatorNone(DummyFilterQueryTranslator):
    def translate_field(self, query, field_name, field_value) -> dict[str, Any]:
        return None


class DummyFilterQueryTranslatorWithIgnoreNoneTrue(DummyFilterQueryTranslator):
    config = FiltererConfigDict(ignore_none=True)


class DummyFilterQueryTranslatorWithIgnoreNoneFalse(DummyFilterQueryTranslator):
    config = FiltererConfigDict(ignore_none=False)


@pytest.mark.parametrize(
    "translator_class, expected",
    [
        pytest.param(DummyFilterQueryTranslator, None, id="ignore_none_default"),
        pytest.param(
            DummyFilterQueryTranslatorWithCustomFieldTranslator, None, id="ignore_none_custom_field_translator"
        ),
        pytest.param(
            DummyFilterQueryTranslatorWithCustomFieldTranslatorNone, None, id="ignore_none_custom_field_translator_nonw"
        ),
        pytest.param(DummyFilterQueryTranslatorWithIgnoreNoneTrue, None, id="ignore_none_true"),
        pytest.param(DummyFilterQueryTranslatorWithIgnoreNoneFalse, {"field": None}, id="ignore_none_false"),
    ],
)
def test_filter_translator__considers_ignore_configs(translator_class, expected):
    translator = translator_class()
    translated_field = translator._translate_field(DummyFilter(), "field")
    assert translated_field == expected


def test_filter_translator_field__should_use_default_resolver_if_not_custom():
    translator = DummyFilterQueryTranslator()
    field_value = "value"
    translated_field = translator._translate_field(DummyFilter(field=field_value), "field")
    assert translated_field == {"field": field_value}


def test_filterer_translate_field__should_use_custom_resolver_if_custom():
    translator = DummyFilterQueryTranslatorWithCustomFieldTranslator()
    translated_field = translator._translate_field(DummyFilter(field="value"), "field")
    assert translated_field == {"field": "custom"}


def test_filterer_translate__should_ignore_none_filter_expressions():
    translator = DummyFilterQueryTranslatorWithCustomFieldTranslatorNone()
    translated = list(translator.translate(query=DummyFilter(field="value", another_field="another_value")))
    assert translated == [{"another_field": "another_value"}]


def test_filter_query_base_translator__should_translate_all_fields():
    translator = DummyFilterQueryTranslator()
    translated = list(translator.translate(query=DummyFilter(field="value", another_field="another_value")))
    assert translated == [{"field": "value"}, {"another_field": "another_value"}]
