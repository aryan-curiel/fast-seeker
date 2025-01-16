from odmantic import Model as ODManticModel
from odmantic.query import SortExpression, asc, desc

from fast_seeker.core.sorting import OrderBuilder, SortDirection, SortingModel

ODMANTIC_DIRECTION_MAP = {
    SortDirection.ASC: asc,
    SortDirection.DESC: desc,
}


ODManticSortArgs = tuple[SortExpression, ...]


class ODManticOrderBuilder(OrderBuilder[ODManticSortArgs]):
    def get_order(self, model: type[ODManticModel], sort_query: SortingModel) -> ODManticSortArgs:
        return tuple(ODMANTIC_DIRECTION_MAP[entry.direction](getattr(model, entry.key)) for entry in sort_query.parsed)
