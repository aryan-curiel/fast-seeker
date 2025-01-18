from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel, ConfigDict

from .base import QueryProcessor


class FilterModel(BaseModel):
    model_config = ConfigDict(json_schema_extra={"ignore_none": True})


class Filterer[_TData, _TResult, _TFilterExpression](
    QueryProcessor[_TData, FilterModel, _TResult, _TFilterExpression], ABC
):
    @abstractmethod
    def default_resolver(
        self, data: _TData, query: FilterModel, field_name: str, field_value: Any
    ) -> _TFilterExpression: ...

    def translate(self, data: _TData, query: FilterModel) -> Iterable[_TFilterExpression]:
        model_config_extra = query.model_config.get("json_schema_extra", {})
        for field_name, field_info in query.model_fields.items():
            ignore_none = (field_info.json_schema_extra or model_config_extra).get("ignore_none", True)
            field_value = getattr(query, field_name)
            if field_value is None and ignore_none:
                continue
            custom_field_resolver = getattr(query, f"resolve_{field_name}", None)
            filter_expression = (
                custom_field_resolver(field_name, field_value)
                if custom_field_resolver
                else self.default_resolver(query, field_name, field_value)
            )
            if filter_expression:
                yield filter_expression
