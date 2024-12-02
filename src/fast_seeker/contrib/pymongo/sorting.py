from pymongo import ASCENDING, DESCENDING
from pymongo.cursor import Cursor

from fast_seeker.core.sorting import SortDirection, Sorter

PYMONGO_DIRECTION_MAP = {
    SortDirection.ASC: ASCENDING,
    SortDirection.DESC: DESCENDING,
}


class ODManticSorter(Sorter[Cursor, Cursor]):
    def _apply_order(self, cursor: Cursor, order: list[tuple[str, SortDirection]]) -> Cursor:
        return cursor.sort([(key, PYMONGO_DIRECTION_MAP[direction]) for key, direction in order])
