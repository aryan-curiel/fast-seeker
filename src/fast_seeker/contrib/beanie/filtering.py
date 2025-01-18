from collections.abc import Iterable
from typing import Any

from beanie.odm.queries.find import FindMany

from fast_seeker.core.filtering import Filterer, FilterModel


class BeanieFilterer(Filterer[FindMany, FindMany, Iterable[dict[str, Any]]]):
    def translate(self, query: FilterModel) -> Iterable[dict[str, Any]]:
        model_config_extra = query.model_config.get("json_schema_extra", {})
        for field_name, field_info in query.model_fields.items():
            ignore_none = (field_info.json_schema_extra or model_config_extra).get("ignore_none", True)
            field_value = getattr(query, field_name)
            if field_value is None and ignore_none:
                continue
            # TODO: Implement custom resolver functions or field translators
            yield {field_name: field_value}

    def execute(self, data: FindMany, args: Iterable[dict[str, Any]]) -> FindMany:
        return data.find(*args)
