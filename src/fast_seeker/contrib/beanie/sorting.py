from beanie.odm.enums import SortDirection as BeanieSortDirection
from beanie.odm.queries.find import FindMany

from fast_seeker.core.sorting import SortDirection, Sorter, SortingModel

BEANIE_DIRECTION_MAP = {
    SortDirection.ASC: BeanieSortDirection.ASCENDING,
    SortDirection.DESC: BeanieSortDirection.DESCENDING,
}


BeanieSortArgs = str | tuple[str, BeanieSortDirection] | list[tuple[str, BeanieSortDirection]]


def beanie_sorting_translator(query: SortingModel) -> BeanieSortArgs:
    return [(entry.key, BEANIE_DIRECTION_MAP[entry.direction]) for entry in query.parsed]


def beanie_sorting_executor(data: FindMany, order: BeanieSortArgs) -> FindMany:
    return data.sort(order)


class BeanieSorter(Sorter[FindMany, FindMany, BeanieSortArgs]):
    def __init__(self):
        super().__init__(translator=beanie_sorting_translator, executor=beanie_sorting_executor)
