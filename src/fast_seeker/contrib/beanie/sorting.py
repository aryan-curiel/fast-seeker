from beanie.odm.enums import SortDirection as BeanieSortDirection
from beanie.odm.queries.find import FindMany

from fast_seeker.core.sorting import SortDirection, Sorter, SortingQuery

BEANIE_DIRECTION_MAP = {
    SortDirection.ASC: BeanieSortDirection.ASCENDING,
    SortDirection.DESC: BeanieSortDirection.DESCENDING,
}


BeanieSortArgs = list[tuple[str, BeanieSortDirection]]


class BeanieSorter(Sorter[FindMany, FindMany, BeanieSortArgs]):
    def translate(self, data: FindMany, query: SortingQuery) -> BeanieSortArgs:
        return [(entry.key, BEANIE_DIRECTION_MAP[entry.direction]) for entry in query.parsed]

    def execute(self, data: FindMany, order: BeanieSortArgs) -> FindMany:
        return data.sort(order)
