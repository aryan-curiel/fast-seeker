from collections.abc import Iterable
from typing import Any

from beanie.odm.queries.find import FindMany

from fast_seeker.core.base import QueryExecutor
from fast_seeker.core.filtering import Filterer, FilterQuery, FilterQueryBaseTranslator

BeanieFilterEntry = dict[str, Any]


class BeanieFilterQueryTranslator(FilterQueryBaseTranslator[BeanieFilterEntry]):
    def _default_field_translator(
        self, query: FilterQuery, field_name: str, field_value: Any, **kwargs
    ) -> BeanieFilterEntry:
        return {field_name: field_value}


class BeanieFilterQueryExecutor(QueryExecutor[FindMany, Iterable[BeanieFilterEntry]]):
    def __call__(self, *, source: FindMany, translated_query: Iterable[BeanieFilterEntry], **kwargs) -> FindMany:
        return source.find(*translated_query)


class BeanieFilterer(Filterer[FindMany, BeanieFilterEntry]):
    translator = BeanieFilterQueryTranslator()
    executor = BeanieFilterQueryExecutor()
