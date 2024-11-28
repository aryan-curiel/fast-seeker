from pydantic import Field

from fast_seeker.contrib.beanie.filtering import BeanieFilterer, FilterModel

from .utils import DummyFindMany


class DummyFilterQueryWithoutNone(FilterModel):
    field1: str | None = None
    field2: str | None = None


def test_beanie_filterer_filter__should_filter_data_and_ignore_none_by_default():
    filterer = BeanieFilterer()
    data = DummyFindMany()
    filter_query = DummyFilterQueryWithoutNone(field1="value1")
    result = filterer.filter(data, filter_query)
    assert result.find_expressions == [{"field1": "value1"}]


class DummyFilterQueryWithFieldNone(FilterModel):
    field1: str | None = None
    field2: str | None = Field(None, json_schema_extra={"ignore_none": False})


def test_beanie_filterer_filter__should_filter_data_and_not_ignore_none_when_specified():
    filterer = BeanieFilterer()
    data = DummyFindMany()
    filter_query = DummyFilterQueryWithFieldNone(field1="value1", field2=None)
    result = filterer.filter(data, filter_query)
    assert result.find_expressions == [{"field1": "value1"}, {"field2": None}]
