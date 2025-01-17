from django.db.models import QuerySet

from fast_seeker.core.sorting import Sorter, SortingQuery


def django_sorting_translator(query: SortingQuery) -> list[str]:
    return query.order_by


def django_sorting_executor(data: QuerySet, order: list[str]) -> QuerySet:
    return data.order_by(*order)


class QuerySetSorter(Sorter[QuerySet, QuerySet, list[str]]):
    def __init__(self):
        super().__init__(translator=django_sorting_translator, executor=django_sorting_executor)
