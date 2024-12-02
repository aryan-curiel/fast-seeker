from beanie.odm.enums import SortDirection as BeanieSortDirection
from beanie.odm.queries.find import FindMany

from fast_seeker.core.sorting import SortDirection, Sorter

BEANIE_DIRECTION_MAP = {
    SortDirection.ASC: BeanieSortDirection.ASCENDING,
    SortDirection.DESC: BeanieSortDirection.DESCENDING,
}


class BeanieSorter(Sorter[FindMany, FindMany]):
    def _apply_order(self, data: FindMany, order: list[tuple[str, SortDirection]]) -> FindMany:
        return data.sort([(key, BEANIE_DIRECTION_MAP[direction]) for key, direction in order])
