from odmantic import Model as ODManticModel
from odmantic.query import SortExpression, asc, desc

from fast_seeker.core.sorting import SortDirection, Sorter

ODMANTIC_DIRECTION_MAP = {
    SortDirection.ASC: asc,
    SortDirection.DESC: desc,
}


class ODManticSorter(Sorter[type[ODManticModel], tuple[SortExpression, ...]]):
    def _apply_order(
        self, data: type[ODManticModel], order: list[tuple[str, SortDirection]]
    ) -> tuple[SortExpression, ...]:
        sort_expressions: list[SortExpression] = []
        for key, direction in order:
            model_field = getattr(data, key, None)
            if not model_field:
                raise ValueError(f"Field {key} does not exist on model {data}")
            sort_expressions.append(ODMANTIC_DIRECTION_MAP[direction](model_field))
        return tuple(sort_expressions)
