from django.db.models import QuerySet

from fast_seeker.core.sorting import Sorter, SortingQuery


class QuerySetSorter(Sorter[QuerySet, QuerySet, list[str]]):
    def translate(self, query: SortingQuery) -> list[str]:
        return query.order_by

    def execute(self, data: QuerySet, order: list[str]) -> QuerySet:
        return data.order_by(*order)
