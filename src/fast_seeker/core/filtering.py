from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel, ConfigDict

from .base import QueryProcessor


class FiltererConfigDict(ConfigDict):
    ignore_none: bool = True


class FilterModel(BaseModel):
    model_config = FiltererConfigDict()


class Filterer[_TData, _TResult, _TFilterExpression](
    QueryProcessor[_TData, FilterModel, _TResult, _TFilterExpression], ABC
):
    @abstractmethod
    def default_resolver(
        self, data: _TData, query: FilterModel, field_name: str, field_value: Any
    ) -> _TFilterExpression: ...

    def translate_field(self, data: _TData, query: FilterModel, field_name: str) -> _TFilterExpression:
        ignore_none = (query.model_fields[field_name].json_schema_extra or query.model_config).get("ignore_none", True)
        field_value = getattr(query, field_name)
        if field_value is None and ignore_none:
            return None
        custom_field_resolver = getattr(query, f"resolve_{field_name}", None)
        filter_expression = (
            custom_field_resolver(field_name, field_value, data)
            if custom_field_resolver
            else self.default_resolver(data, query, field_name, field_value)
        )
        return filter_expression

    def translate(self, data: _TData, query: FilterModel) -> Iterable[_TFilterExpression]:
        for field_name in query.model_fields:
            filter_expression = self.translate_field(data, query, field_name)
            if filter_expression:
                yield filter_expression
