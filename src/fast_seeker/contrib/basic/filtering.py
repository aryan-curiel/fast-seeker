from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel

from fast_seeker.core.filtering import Filterer


class DictIterableFilterer(Filterer[Iterable[dict], Iterable[dict]]):
    def filter(self, data: Iterable[dict], filter_query: BaseModel) -> Iterable[dict]:
        filtered_data = data
        for field_name, _ in filter_query.model_fields.items():
            field_value = getattr(filter_query, field_name)
            if field_value is None:
                continue
            filtered_data = [elem for elem in filtered_data if elem.get(field_name) == field_value]
        return filtered_data


class ObjectIterableFilterer(Filterer[Iterable[Any], Iterable[Any]]):
    def filter(self, data: Iterable[Any], filter_query: BaseModel) -> Iterable[Any]:
        filtered_data = data
        for field_name, _ in filter_query.model_fields.items():
            field_value = getattr(filter_query, field_name)
            if field_value is None:
                continue
            filtered_data = [elem for elem in filtered_data if getattr(elem, field_name) == field_value]
        return filtered_data
