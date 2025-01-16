from django.db.models import QuerySet

from fast_seeker.core.sorting import SortDirection, Sorter

DJANGO_DIRECTION_MAP = {
    SortDirection.ASC: "",
    SortDirection.DESC: "-",
}


class QuerySetSorter(Sorter[QuerySet, QuerySet]):
    def _apply_order(self, data: QuerySet, order: list[tuple[str, SortDirection]]) -> QuerySet:
        return data.order_by(*[f"{DJANGO_DIRECTION_MAP[direction]}{key}" for key, direction in order])
