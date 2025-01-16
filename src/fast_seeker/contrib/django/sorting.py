from django.db.models import QuerySet

from fast_seeker.core.sorting import Sorter, SortingModel


class QuerySetSorter(Sorter[QuerySet, QuerySet, list[str]]):
    def get_order(self, sort_query: SortingModel) -> list[str]:
        return sort_query.order_by

    def _apply_order(self, data: QuerySet, order: list[str]) -> QuerySet:
        return data.order_by(*order)
