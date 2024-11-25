from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, ClassVar, Generic, TypedDict, TypeVar, Union

from pydantic import BaseModel

from .base import QueryProcessor, QueryTranslator, _TData

_TFilterExpression = TypeVar("_TFilterExpression")


class FiltererConfigDict(TypedDict, total=False):
    ignore_none: bool


class FilterQuery(BaseModel): ...


class FilterQueryBaseTranslator(
    QueryTranslator[FilterQuery, Iterable[_TFilterExpression]], Generic[_TFilterExpression]
):
    config: ClassVar[FiltererConfigDict] = FiltererConfigDict(ignore_none=True)

    @abstractmethod
    def _default_field_translator(
        self, query: FilterQuery, field_name: str, field_value: Any, **kwargs
    ) -> _TFilterExpression: ...

    def _translate_field(self, query: FilterQuery, field_name: str, **kwargs) -> Union[_TFilterExpression, None]:
        ignore_none = self.config.get("ignore_none", True)
        field_value = getattr(query, field_name)
        if field_value is None and ignore_none:
            return None
        custom_field_translator = getattr(self, f"translate_{field_name}", None)
        field_translator = custom_field_translator or self._default_field_translator
        return field_translator(query, field_name, field_value, **kwargs)

    def __call__(self, *, query: FilterQuery, **kwargs) -> Iterable[_TFilterExpression]:
        for field_name in query.model_fields:
            filter_expression = self._translate_field(query, field_name, **kwargs)
            if filter_expression:
                yield filter_expression


class Filterer(
    QueryProcessor[FilterQuery, Iterable[_TFilterExpression], _TData],
    Generic[_TData, _TFilterExpression],
): ...
