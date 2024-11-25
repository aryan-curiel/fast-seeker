from collections.abc import Iterable

from beanie.odm.enums import SortDirection as BeanieSortDirection
from beanie.odm.queries.find import FindMany

from fast_seeker.core.base import QueryExecutor
from fast_seeker.core.sorting import (
    SortDirection,
    Sorter,
    SortingQuery,
    SortingQueryBaseTranslator,
)

BEANIE_DIRECTION_MAP = {
    SortDirection.ASC: BeanieSortDirection.ASCENDING,
    SortDirection.DESC: BeanieSortDirection.DESCENDING,
}


BeanieSortArgs = Iterable[tuple[str, BeanieSortDirection]]


class BeanieSortingQueryTranslator(SortingQueryBaseTranslator[BeanieSortArgs]):
    def __call__(self, *, query: SortingQuery, **kwargs) -> BeanieSortArgs:
        for entry in self._translate_as_entries(query):
            yield entry.key, BEANIE_DIRECTION_MAP[entry.direction]


class BeanieSortingQueryExecutor(QueryExecutor[FindMany, BeanieSortArgs]):
    def __call__(self, *, source: FindMany, translated_query: BeanieSortArgs, **kwargs) -> FindMany:
        return source.sort(*translated_query)


class BeanieSorter(Sorter[FindMany, BeanieSortArgs]):
    translator = BeanieSortingQueryTranslator()
    executor = BeanieSortingQueryExecutor()
