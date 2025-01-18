from abc import ABC
from collections.abc import Generator
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from pydantic import BaseModel

from .base import QueryProcessor

ASC_SIGN = "+"
DESC_SIGN = "-"


class SortDirection(StrEnum):
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


GenericOrdering = list[tuple[str, SortDirection]]


class SortingQuery(BaseModel):
    order_by: list[str] = []

    @classmethod
    def _parse_entry(cls, order: str) -> OrderEntry:
        order = order if order.startswith((ASC_SIGN, DESC_SIGN)) else f"{ASC_SIGN}{order}"
        return OrderEntry(key=order[1:], direction=SortDirection(order[0]))

    @property
    def parsed(self) -> Generator[OrderEntry]:
        return (SortingQuery._parse_entry(order) for order in self.order_by)


class Sorter[_TData, _TResult, _TSortArgs](QueryProcessor[_TData, SortingQuery, _TResult, _TSortArgs], ABC): ...
