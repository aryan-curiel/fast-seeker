from typing import Any

from odmantic.query import QueryExpression

from fast_seeker.core.filtering import Filterer, FilterModel

from .engines import ODManticFindQueryBuilder

ODMQueryExpressions = QueryExpression | dict | bool


class ODManticFilterer(Filterer[ODManticFindQueryBuilder, ODManticFindQueryBuilder, ODMQueryExpressions]):
    def default_resolver(
        self, data: ODManticFindQueryBuilder, query: FilterModel, field_name: str, field_value: Any
    ) -> ODMQueryExpressions:
        return getattr(data.model, field_name) == field_value

    def execute(self, data: ODManticFindQueryBuilder, args: ODMQueryExpressions) -> ODManticFindQueryBuilder:
        return data.filter(*args)
