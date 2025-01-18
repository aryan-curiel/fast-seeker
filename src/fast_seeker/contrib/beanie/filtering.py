from collections.abc import Iterable
from typing import Any

from beanie.odm.queries.find import FindMany

from fast_seeker.core.filtering import Filterer, FilterModel


class BeanieFilterer(Filterer[FindMany, FindMany, dict[str, Any]]):
    def default_resolver(self, data: FindMany, query: FilterModel, field_name: str, field_value: Any) -> dict[str, Any]:
        return {field_name: field_value}

    def execute(self, data: FindMany, args: Iterable[dict[str, Any]]) -> FindMany:
        return data.find(*args)
