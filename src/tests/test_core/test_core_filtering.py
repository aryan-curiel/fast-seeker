from typing import Any

import pytest
from pydantic import Field

from fast_seeker.core.filtering import Filterer, FiltererConfigDict, FilterModel


class DummyFilterDefault(FilterModel):
    field: str | None = None


class DummyFilterWithCustomResolver(FilterModel):
    field: str | None = None

    def resolve_field(self, field_name: str, field_value: Any, data: Any) -> dict[str, Any]:
        return {field_name: "custom"}


class DummyFilterWithCustomResolverNone(FilterModel):
    field: str | None = None

    def resolve_field(self, field_name: str, field_value: Any, data: Any) -> dict[str, Any]:
        return None


class DummyFilterIgnoreNoneTrue(FilterModel):
    model_config = FiltererConfigDict(ignore_none=True)
    field: str | None = None


class DummyFilterIgnoreNoneFalse(FilterModel):
    model_config = FiltererConfigDict(ignore_none=False)
    field: str | None = None


class DummyFilterWithFieldIgnoreNoneFalse(FilterModel):
    field: str | None = Field(None, json_schema_extra={"ignore_none": False})


class DummyFilterWithFieldIgnoreNoneTrue(FilterModel):
    model_config = FiltererConfigDict(ignore_none=False)
    field: str | None = Field(None, json_schema_extra={"ignore_none": True})


class DummyFilterer(Filterer[Any, Any, dict[str, Any]]):
    def default_resolver(self, data, query, field_name, field_value) -> dict[str, Any]:
        return {field_name: field_value}

    def execute(self, data, args) -> Any: ...


@pytest.mark.parametrize(
    "filter_query, field_name, expected",
    [
        pytest.param(DummyFilterDefault(), "field", None, id="ignore_none_default"),
        pytest.param(DummyFilterIgnoreNoneTrue(), "field", None, id="ignore_none_true"),
        pytest.param(DummyFilterIgnoreNoneFalse(), "field", {"field": None}, id="ignore_none_false"),
        pytest.param(DummyFilterWithFieldIgnoreNoneFalse(), "field", {"field": None}, id="field_ignore_none_false"),
        pytest.param(DummyFilterWithFieldIgnoreNoneTrue(), "field", None, id="field_ignore_none_true"),
    ],
)
def test_filterer_translate_field_ignore_none_values(filter_query, field_name, expected):
    translated_field = DummyFilterer().translate_field(None, filter_query, field_name)
    assert translated_field == expected


def test_filterer_translate_field__should_use_default_resolver_if_not_custom():
    field_value = "value"
    translated_field = DummyFilterer().translate_field(None, DummyFilterDefault(field=field_value), "field")
    assert translated_field == {"field": field_value}


def test_filterer_translate_field__should_use_custom_resolver_if_custom():
    translated_field = DummyFilterer().translate_field(None, DummyFilterWithCustomResolver(field="value"), "field")
    assert translated_field == {"field": "custom"}


def test_filterer_translate__should_ignore_none_filter_expressions():
    translated = list(DummyFilterer().translate(None, DummyFilterWithCustomResolverNone(field="value")))
    assert translated == []


def test_filterer_translate__should_translate_all_fields():
    translated = list(DummyFilterer().translate(None, DummyFilterDefault(field="value")))
    assert translated == [{"field": "value"}]
