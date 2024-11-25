from collections.abc import Iterable
from typing import Any

from django.db.models import Q, QuerySet

from fast_seeker.core.base import QueryExecutor
from fast_seeker.core.filtering import Filterer, FilterQuery, FilterQueryBaseTranslator


class DjangoFilterQueryTranslator(FilterQueryBaseTranslator[Q]):
    def _default_field_translator(self, query: FilterQuery, field_name: str, field_value: Any, **kwargs) -> Q:
        return Q(**{field_name: field_value})


class DjangoFilterQueryExecutor(QueryExecutor[QuerySet, Q]):
    def __call__(self, *, source: QuerySet, translated_query: Iterable[Q], **kwargs) -> QuerySet:
        return source.filter(*translated_query)


class DjangoFilterer(Filterer[QuerySet, Q]):
    translator = DjangoFilterQueryTranslator()
    executor = DjangoFilterQueryExecutor()
