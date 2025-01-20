from odmantic.query import SortExpression, asc, desc

from fast_seeker.core.sorting import SortDirection, Sorter, SortingQuery

from .engines import ODManticFindQueryBuilder

ODMANTIC_DIRECTION_MAP = {
    SortDirection.ASC: asc,
    SortDirection.DESC: desc,
}


ODManticSortArgs = tuple[SortExpression, ...]


class ODManticSorter(Sorter[ODManticFindQueryBuilder, ODManticFindQueryBuilder, ODManticSortArgs]):
    def translate(self, data: ODManticFindQueryBuilder, query: SortingQuery) -> ODManticSortArgs:
        return tuple(ODMANTIC_DIRECTION_MAP[entry.direction](getattr(data.model, entry.key)) for entry in query.parsed)

    def execute(self, data: ODManticFindQueryBuilder, args: ODManticSortArgs) -> ODManticFindQueryBuilder:
        return data.sort(args)
