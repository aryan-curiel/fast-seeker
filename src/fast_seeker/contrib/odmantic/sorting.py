from odmantic.query import SortExpression, asc, desc

from fast_seeker.core.base import QueryProcessor
from fast_seeker.core.sorting import SortDirection, SortingQuery

from .engines import ODManticFindQueryBuilder

ODMANTIC_DIRECTION_MAP = {
    SortDirection.ASC: asc,
    SortDirection.DESC: desc,
}


ODManticSortArgs = tuple[SortExpression, ...]


class ODManticSorter(QueryProcessor[ODManticFindQueryBuilder, ODManticFindQueryBuilder, ODManticSortArgs]):
    def translate(self, data: ODManticFindQueryBuilder, query: SortingQuery) -> ODManticSortArgs:
        return tuple(ODMANTIC_DIRECTION_MAP[entry.direction](getattr(self._model, entry.key)) for entry in query.parsed)

    def execute(self, data: ODManticFindQueryBuilder, args: ODManticSortArgs) -> ODManticFindQueryBuilder:
        return data.sort(args)
