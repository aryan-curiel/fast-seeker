from collections.abc import Iterable
from typing import Any

from motor.core import AgnosticCollection as Collection
from motor.core import AgnosticCursor as Cursor

from fast_seeker.core.filtering import Filterer, FilterModel


class MotorFilterer(Filterer[Collection, Cursor, dict[str, Any]]):
    def default_resolver(
        self, data: Collection, query: FilterModel, field_name: str, field_value: Any
    ) -> dict[str, Any]:
        return {field_name: field_value}

    def execute(self, data: Collection, args: Iterable[dict[str, Any]]) -> Cursor:
        return data.find(*args)