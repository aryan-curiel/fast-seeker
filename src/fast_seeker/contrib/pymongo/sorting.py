from typing import Literal

from pymongo import ASCENDING, DESCENDING
from pymongo.cursor import Cursor
from pymongo.cursor_shared import _Hint

from fast_seeker.core.sorting import SortDirection, Sorter, SortingModel

PYMONGO_DIRECTION_MAP = {
    SortDirection.ASC: ASCENDING,
    SortDirection.DESC: DESCENDING,
}


PyMongoSortArgs = list[tuple[str, Literal[1] | Literal[-1]]]


class PyMongoSorter(Sorter[Cursor, Cursor, _Hint]):
    def get_order(self, sort_query: SortingModel) -> _Hint:
        return [(entry.key, PYMONGO_DIRECTION_MAP[entry.direction]) for entry in sort_query.parsed]

    def _apply_order(self, cursor: Cursor, order: _Hint) -> Cursor:
        return cursor.sort(order)
