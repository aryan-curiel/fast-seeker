from collections.abc import Iterable
from typing import Any

from django.db.models import Q, QuerySet

from fast_seeker.core.filtering import Filterer, FilterModel


class QuerySetFilterer(Filterer[QuerySet, QuerySet, Q]):
    def default_resolver(self, data: QuerySet, query: FilterModel, field_name: str, field_value: Any) -> Q:
        return Q(**{field_name: field_value})

    def execute(self, data: QuerySet, args: Iterable[Q]) -> QuerySet:
        return data.filter(*args)
