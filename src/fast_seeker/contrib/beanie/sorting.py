import pymongo
from beanie.odm.queries.find import FindMany

from fast_seeker.core.sorting import OrderDirection, Sorter

PYMONGO_DIRECTION_MAP = {
    OrderDirection.ASC: pymongo.ASCENDING,
    OrderDirection.DESC: pymongo.DESCENDING,
}


class BeanieSorter(Sorter[FindMany, FindMany]):
    def _apply_order(self, data: FindMany, order: list[tuple[str, OrderDirection]]) -> FindMany:
        return data.sort([(key, PYMONGO_DIRECTION_MAP[direction]) for key, direction in order])
