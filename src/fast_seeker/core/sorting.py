from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import StrEnum

from pydantic import BaseModel


class SortingModel(BaseModel):
    order_by: list[str] = []


class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


def parse_order_argument(order: str) -> tuple[str, SortDirection]:
    order = order if order.startswith(("+", "-")) else f"+{order}"
    return order[1:], SortDirection.ASC if order[0] == "+" else SortDirection.DESC


class Sorter[_Data, _Result](ABC):
    def _parse_query(
        self,
        sort_query: SortingModel,
        *,
        arg_parser: Callable[[str], tuple[str, SortDirection]] = parse_order_argument,
    ) -> list[tuple[str, SortDirection]]:
        return [arg_parser(order) for order in sort_query.order_by]

    @abstractmethod
    def _apply_order(self, data: _Data, order: list[tuple[str, SortDirection]]) -> _Data:
        raise NotImplementedError

    def sort(
        self,
        data: _Data,
        sort_query: SortingModel,
        *,
        arg_parser: Callable[[str], tuple[str, SortDirection]] = parse_order_argument,
    ) -> _Result:
        if not sort_query.order_by:
            return data
        parsed_query = self._parse_query(sort_query, arg_parser=arg_parser)
        return self._apply_order(data, parsed_query)
