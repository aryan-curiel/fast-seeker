from pymongo.collection import Collection
from pymongo.cursor import Cursor

from fast_seeker.core.filtering import Filterer, FilterModel


class PyMongoFilterer(Filterer[Collection, Cursor]):
    def filter(self, collection: Collection, filter_query: FilterModel, *args, **kwargs) -> Cursor:
        filter_lookups = {}
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
                else {field_name: getattr(filter_query, field_name)}
            )
            if not new_lookup:
                continue
            filter_lookups |= new_lookup
        return collection.find(filter_lookups, *args, **kwargs)
