from collections.abc import Iterable

from django.db.models import QuerySet

from fast_seeker.core.base import QueryExecutor
from fast_seeker.core.sorting import SortDirection, Sorter, SortingQuery, SortingQueryBaseTranslator

DjangoTranslatedQuery = Iterable[str]


class DjangoSortingQueryTranslator(SortingQueryBaseTranslator[DjangoTranslatedQuery]):
    def translate(self, *, query: SortingQuery, **kwargs) -> DjangoTranslatedQuery:
        for entry in self._translate_as_entries(query, **kwargs):
            direction_prefix = "-" if entry.direction == SortDirection.DESC else ""
            yield f"{direction_prefix}{entry.key}"


class DjangoSortingQueryExecutor(QueryExecutor[QuerySet, DjangoTranslatedQuery]):
    def execute(self, *, source: QuerySet, translated_query: DjangoTranslatedQuery, **kwargs):
        return source.order_by(*translated_query)


class DjangoSorter(Sorter[QuerySet, DjangoTranslatedQuery]):
    translator = DjangoSortingQueryTranslator()
    executor = DjangoSortingQueryExecutor()
