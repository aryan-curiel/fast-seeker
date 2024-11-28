from beanie.odm.operators.find.comparison import Eq
from beanie.odm.queries.find import FindMany
from pydantic import BaseModel

from fast_seeker.core.filtering import Filterer


class BeanieFilterer(Filterer[FindMany, FindMany]):
    def filter(self, data: FindMany, filter_query: BaseModel, *args, **kwargs) -> FindMany:
        filter_lookups = []
        for field_name, _ in filter_query.model_fields.items():
            resolver_func = getattr(self, f"resolve_{field_name}", None)
            new_lookup = (
                resolver_func(filter_query, field_name)
                if callable(resolver_func)
                else Eq(field_name, getattr(filter_query, field_name))
            )
            if not new_lookup:
                continue
            if not isinstance(new_lookup, list):
                new_lookup = [new_lookup]
            filter_lookups.extend(new_lookup)
        return data.find(*filter_lookups, *args, **kwargs)
