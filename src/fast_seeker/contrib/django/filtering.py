from collections.abc import Iterable

from django.db.models import Q, QuerySet

from fast_seeker.core.filtering import Filterer, FilterModel


class QuerySetFilterer(Filterer[QuerySet, QuerySet, Iterable[Q]]):
    def translate(self, query: FilterModel) -> Iterable[Q]:
        model_config_extra = query.model_config.get("json_schema_extra", {})
        for field_name, field_info in query.model_fields.items():
            ignore_none = (field_info.json_schema_extra or model_config_extra).get("ignore_none", True)
            field_value = getattr(query, field_name)
            if field_value is None and ignore_none:
                continue
            # TODO: Implement custom resolver functions or field translators
            yield Q(**{field_name: field_value})

    def execute(self, data: QuerySet, args: Iterable[Q]) -> QuerySet:
        return data.filter(*args)
