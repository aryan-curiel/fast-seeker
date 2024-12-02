import pytest
from pydantic import Field

from fast_seeker.contrib.odmantic.filtering import FilterModel, ODManticFilterer

from .utils import DummyDocument


class DummyFilterQueryWithoutNone(FilterModel):
    field1: str | None = None
    field2: str | None = None


class DummyFilterQueryWithFieldNone(FilterModel):
    field1: str | None = None
    field2: str | None = Field(None, json_schema_extra={"ignore_none": False})


class DummyFilterWithResolver(FilterModel):
    field1: str | None = None
    field2: str | None = None

    def resolve_field1(self, field_value, field_info):
        return DummyDocument.field1 == "custom_value"


class DummyFilterWithResolverNone(FilterModel):
    field1: str | None = None
    field2: str | None = None

    def resolve_field1(self, field_value, field_info):
        return None


@pytest.mark.parametrize(
    "filter_query,expected_expressions",
    [
        (DummyFilterQueryWithoutNone(field1="value1"), [{"field1": {"$eq": "value1"}}]),
        (DummyFilterQueryWithFieldNone(field1="value1"), [{"field1": {"$eq": "value1"}}, {"field2": {"$eq": None}}]),
        (DummyFilterWithResolver(field1="value1"), [{"field1": {"$eq": "custom_value"}}]),
        (DummyFilterWithResolverNone(field1="value1"), []),
    ],
)
def test_odmantic_filterer_filter__should_assign_expected_find_expressions(filter_query, expected_expressions):
    filterer = ODManticFilterer()
    result = filterer.filter(DummyDocument, filter_query)
    assert result == expected_expressions
