from fast_seeker.contrib.odmantic.engines import ODManticFindQueryBuilder
from fast_seeker.contrib.odmantic.filtering import ODManticFilterer

from .utils import DummyDocument


def test_odmantic_filterer_default_resolver__should_return_valid_dict(mocker):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    filterer = ODManticFilterer()
    translated_args = filterer.default_resolver(query_builder, None, "field1", "value")
    assert translated_args == {"field1": {"$eq": "value"}}


def test_odmantic_filterer_execute__should_return_filtered_queryset(mocker):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    filterer = ODManticFilterer()
    expressions = [{"field1": {"$eq": "value"}}]
    returned_query_builder = filterer.execute(query_builder, expressions)
    assert returned_query_builder == query_builder
    assert returned_query_builder._filters == [{"field1": {"$eq": "value"}}]
