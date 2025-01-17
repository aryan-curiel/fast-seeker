from typing import Literal

from pymongo import ASCENDING, DESCENDING
from pymongo.cursor import Cursor

from fast_seeker.core.sorting import SortDirection, Sorter, SortingModel

PYMONGO_DIRECTION_MAP = {
    SortDirection.ASC: ASCENDING,
    SortDirection.DESC: DESCENDING,
}


PyMongoSortArgs = list[tuple[str, Literal[1] | Literal[-1]]]


def pymongo_sorting_translator(query: SortingModel) -> PyMongoSortArgs:
    return [(entry.key, PYMONGO_DIRECTION_MAP[entry.direction]) for entry in query.parsed]


def pymongo_sorting_executor(data: Cursor, order: PyMongoSortArgs) -> Cursor:
    return data.sort(order)


class PyMongoSorter(Sorter[Cursor, Cursor, PyMongoSortArgs]):
    def __init__(self):
        super().__init__(translator=pymongo_sorting_translator, executor=pymongo_sorting_executor)
