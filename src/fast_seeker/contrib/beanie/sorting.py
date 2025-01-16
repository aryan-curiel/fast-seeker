from beanie.odm.enums import SortDirection as BeanieSortDirection
from beanie.odm.queries.find import FindMany

from fast_seeker.core.sorting import SortDirection, Sorter, SortingModel

BEANIE_DIRECTION_MAP = {
    SortDirection.ASC: BeanieSortDirection.ASCENDING,
    SortDirection.DESC: BeanieSortDirection.DESCENDING,
}


BeanieSortArgs = str | tuple[str, BeanieSortDirection] | list[tuple[str, BeanieSortDirection]]


class BeanieSorter(Sorter[FindMany, FindMany, BeanieSortArgs]):
    def get_order(self, sort_query: SortingModel) -> BeanieSortArgs:
        return [(entry.key, BEANIE_DIRECTION_MAP[entry.direction]) for entry in sort_query.parsed]

    def _apply_order(self, data: FindMany, order: BeanieSortArgs) -> FindMany:
        return data.sort(order)
