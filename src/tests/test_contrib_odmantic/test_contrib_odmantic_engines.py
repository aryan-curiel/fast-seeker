import pytest
from odmantic.engine import AIOEngine, SyncEngine

from fast_seeker.contrib.odmantic.engines import ODManticFindQueryBuilder, QueryBuilderEngineMixin

from .utils import DummyDocument


def test_odmantic_find_query_builder_ctor(mocker):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    assert query_builder.engine is not None
    assert query_builder.model is not None
    assert query_builder._filters == []
    assert query_builder._sort is None
    assert query_builder._skip == 0
    assert query_builder._limit is None


def test_odmantic_find_query_builder_filter(mocker):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    query_builder.filter([{"field1": {"$eq": "value"}}])
    assert query_builder._filters == [{"field1": {"$eq": "value"}}]


def test_odmantic_find_query_builder_sort(mocker):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    query_builder.sort({"field1": 1})
    assert query_builder._sort == {"field1": 1}


def test_odmantic_find_query_builder_skip(mocker):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    query_builder.skip(10)
    assert query_builder._skip == 10


def test_odmantic_find_query_builder_limit(mocker):
    query_builder = ODManticFindQueryBuilder(mocker.MagicMock(), DummyDocument)
    query_builder.limit(10)
    assert query_builder._limit == 10


@pytest.mark.parametrize(
    "engine_class",
    [
        AIOEngine,
        SyncEngine,
    ],
)
def test_odmantic_find_query_builder_find__should_be_called_with_query_builder_fields(engine_class, mocker):
    filters, sorting, skip, limit = [{"field1": {"$eq": "value"}}], {"field1": 1}, 10, 10
    mocked_engine = mocker.MagicMock(spec=engine_class)
    query_builder = ODManticFindQueryBuilder(mocked_engine, DummyDocument)
    query_builder._filters = filters
    query_builder._sort = sorting
    query_builder._skip = skip
    query_builder._limit = limit
    query_builder.find(DummyDocument)
    mocked_engine.find.assert_called_with(DummyDocument, *filters, sort=sorting, skip=skip, limit=limit, session=None)


@pytest.mark.parametrize(
    "engine_class",
    [
        AIOEngine,
        SyncEngine,
    ],
)
def test_odmantic_find_query_builder_find__should_be_called_with_args_if_passed(engine_class, mocker):
    filters, sorting, skip, limit = [{"field2": {"$eq": "value"}}], {"field1": 1}, 10, 10
    mocked_engine = mocker.MagicMock(spec=engine_class)
    query_builder = ODManticFindQueryBuilder(mocked_engine, DummyDocument)
    query_builder._filters = [{"field1": {"$eq": "value"}}]
    query_builder._sort = {"field1": -1}
    query_builder._skip = 5
    query_builder._limit = 5
    query_builder.find(DummyDocument, *filters, sort=sorting, skip=skip, limit=limit)
    mocked_engine.find.assert_called_with(
        DummyDocument, *query_builder._filters, *filters, sort=sorting, skip=skip, limit=limit, session=None
    )


def test_query_builder_engine_mixin_query_for__should_return_valid_query_builder(mocker):
    mocked_engine = mocker.MagicMock(spec=SyncEngine)
    query_builder = QueryBuilderEngineMixin.query_for(mocked_engine, DummyDocument)
    assert query_builder.engine == mocked_engine
    assert query_builder.model == DummyDocument
