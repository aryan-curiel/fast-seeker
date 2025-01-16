import pytest
from django.db.models import QuerySet
from pydantic import Field

from fast_seeker.contrib.django.filtering import FilterModel, QuerySetFilterer


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
        return {"field1": "custom_value"}


class DummyFilterWithResolverNone(FilterModel):
    field1: str | None = None
    field2: str | None = None

    def resolve_field1(self, field_value, field_info):
        return None


@pytest.mark.parametrize(
    "filter_query,expected_expressions",
    [
        (DummyFilterQueryWithoutNone(field1="value1"), {"field1": "value1"}),
        (DummyFilterQueryWithFieldNone(field1="value1"), {"field1": "value1", "field2": None}),
        (DummyFilterWithResolver(field1="value1"), {"field1": "custom_value"}),
        (DummyFilterWithResolverNone(field1="value1"), {}),
    ],
)
def test_django_filterer_filter__should_assign_expected_find_expressions(filter_query, expected_expressions, mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)
    filterer = QuerySetFilterer()
    filterer.filter(mock_queryset, filter_query)
    mock_queryset.filter.assert_called_once_with(**expected_expressions)
