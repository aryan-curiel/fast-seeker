from collections.abc import Iterable
from typing import Any

from odmantic.engine import (
    AIOCursor,
    AIOEngine,
    AIOSessionType,
    BaseCursor,
    BaseEngine,
    ModelType,
    SyncCursor,
    SyncEngine,
    SyncSessionType,
)
from odmantic.query import QueryExpression


class ODManticFindQueryBuilder[
    _TEngine: BaseEngine,
    _TSession: (AIOSessionType, SyncSessionType),
    _TCursor: BaseCursor,
]:
    def __init__(self, engine: _TEngine, model: type[ModelType]):
        self.engine = engine
        self.model = model
        self._filters: list[QueryExpression | dict | bool] = []
        self._sort: Any | None = None
        self._skip: int = 0
        self._limit: int | None = None

    def filter(self, queries: Iterable[QueryExpression | dict | bool]):
        self._filters.extend(queries)
        return self

    def sort(self, sort: Any):
        self._sort = sort
        return self

    def skip(self, skip: int):
        self._skip = skip
        return self

    def limit(self, limit: int):
        self._limit = limit
        return self

    def find(
        self,
        model: type[ModelType],
        *queries: QueryExpression | dict | bool,
        sort: Any | None = None,
        skip: int = 0,
        limit: int | None = None,
        session: _TSession = None,
    ) -> _TCursor:
        return self.engine.find(
            model,
            *self._filters,
            *queries,
            sort=sort or self._sort,
            skip=skip or self._skip,
            limit=limit or self._limit,
            session=session,
        )


class QueryBuilderEngineMixin[_TEngine, _TSession, _TCursor]:
    def query_for(self: _TEngine, model: type[ModelType]) -> ODManticFindQueryBuilder[_TEngine, _TSession, _TCursor]:
        return ODManticFindQueryBuilder(self, model)


class SeekerAIOEngine(AIOEngine, QueryBuilderEngineMixin[AIOEngine, AIOSessionType, AIOCursor[ModelType]]): ...


class SeekerSyncEngine(SyncEngine, QueryBuilderEngineMixin[SyncEngine, SyncSessionType, SyncCursor[ModelType]]): ...
