from collections.abc import Iterable

from odmantic import Model as ODManticModel
from odmantic.query import QueryExpression

from fast_seeker.core.filtering import Filterer, FilterModel


class ODManticFilterer(Filterer[type[ODManticModel], Iterable[QueryExpression]]):
    def filter(
        self, data: type[ODManticModel], filter_query: FilterModel, *args, **kwargs
    ) -> Iterable[QueryExpression]:
        filter_lookups = []
        for field_name, field_info in filter_query.model_fields.items():
            resolver_func = getattr(filter_query, f"resolve_{field_name}", None)
            field_extra = field_info.json_schema_extra or filter_query.model_config.get("json_schema_extra", {})
            ignore_none = field_extra.get("ignore_none", True)
            field_value = getattr(filter_query, field_name)
            if field_value is None and ignore_none:
                continue
            new_lookup = (
                resolver_func(field_value, field_info)
                if callable(resolver_func)
                else getattr(data, field_name) == field_value
            )
            if not new_lookup:
                continue
            if not isinstance(new_lookup, list):
                new_lookup = [new_lookup]
            filter_lookups.extend(new_lookup)
        return filter_lookups
