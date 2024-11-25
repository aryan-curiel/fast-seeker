from collections.abc import Iterable
from typing import Any

from fast_seeker.core.sorting import OrderDirection, Sorter


class DictIterableSorter(Sorter[Iterable[dict], Iterable[dict]]):  # TODO: remake this class
    def _apply_order(self, data: Iterable[dict], order: list[tuple[str, OrderDirection]]) -> Iterable[dict]:
        return sorted(data, key=lambda x: tuple(x.get(order[0]) for order in order))


class ObjectIterableSorter(Sorter[Iterable[Any], Iterable[Any]]):  # TODO: remake this class
    def _apply_order(self, data: Iterable[Any], order: list[tuple[str, OrderDirection]]) -> Iterable[Any]:
        return sorted(data, key=lambda x: tuple(getattr(x, order[0]) for order in order))
