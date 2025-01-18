from typing import Literal

from pymongo import ASCENDING, DESCENDING
from pymongo.cursor import Cursor

from fast_seeker.core.sorting import SortDirection, Sorter, SortingQuery

PYMONGO_DIRECTION_MAP = {
    SortDirection.ASC: ASCENDING,
    SortDirection.DESC: DESCENDING,
}


PyMongoSortArgs = list[tuple[str, Literal[1] | Literal[-1]]]


class PyMongoSorter(Sorter[Cursor, Cursor, PyMongoSortArgs]):
    def translate(self, data: Cursor, query: SortingQuery) -> PyMongoSortArgs:
        return [(entry.key, PYMONGO_DIRECTION_MAP[entry.direction]) for entry in query.parsed]

    def execute(self, data: Cursor, order: PyMongoSortArgs) -> Cursor:
        return data.sort(order)
