from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Generic, TypedDict, Union

from pydantic import BaseModel
from typing_extensions import Self

from .base import QueryProcessor, QueryTranslator, _TData, _TTranslationResult

ASC_SIGN = "+"
DESC_SIGN = "-"


class SortDirection(Enum):
    ASC = ASC_SIGN
    DESC = DESC_SIGN


@dataclass
class OrderEntry:
    key: str
    direction: SortDirection

    @classmethod
    def asc(cls, key: str) -> Self:
        return cls(key=key, direction=SortDirection.ASC)

    @classmethod
    def desc(cls, key: str) -> Self:
        return cls(key=key, direction=SortDirection.DESC)


class SortingQuery(BaseModel):
    order_by: list[str] = []


class TranslatorConfigDict(TypedDict, total=False):
    field_translators: dict[str, Union[str, Callable[[SortingQuery, OrderEntry], OrderEntry]]]


class SortingQueryBaseTranslator(QueryTranslator[SortingQuery, _TTranslationResult], Generic[_TTranslationResult]):
    config: ClassVar[TranslatorConfigDict] = TranslatorConfigDict(field_translators={})

    @classmethod
    def _parse_entry(cls, order: str) -> OrderEntry:
        order = order if order.startswith((ASC_SIGN, DESC_SIGN)) else f"{ASC_SIGN}{order}"
        return OrderEntry(key=order[1:], direction=SortDirection(order[0]))

    def _translate_entry(self, query: SortingQuery, entry: OrderEntry) -> OrderEntry:
        class_field_translator = getattr(self, f"translate_{entry.key}", None)
        if class_field_translator:
            return class_field_translator(query, entry)
        config_translator = self.config.get("field_translators", {}).get(entry.key, None)
        if not config_translator:
            return entry
        if isinstance(config_translator, str):
            return OrderEntry(key=config_translator, direction=entry.direction)
        if callable(config_translator):
            return config_translator(query, entry)
        raise ValueError(f"Invalid translator for {entry.key}: f{config_translator}")

    def _translate_as_entries(self, query: SortingQuery) -> Iterable[OrderEntry]:
        for order_value in query.order_by:
            parsed_entry = self._parse_entry(order_value)
            yield self._translate_entry(query, parsed_entry)


class Sorter(
    QueryProcessor[SortingQuery, _TTranslationResult, _TData],
    Generic[_TData, _TTranslationResult],
): ...
