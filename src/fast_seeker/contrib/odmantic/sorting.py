from typing import Self

from odmantic import Model as ODManticModel
from odmantic.query import SortExpression, asc, desc

from fast_seeker.core.base import QueryTranslator
from fast_seeker.core.sorting import SortDirection, SortingQuery

ODMANTIC_DIRECTION_MAP = {
    SortDirection.ASC: asc,
    SortDirection.DESC: desc,
}


ODManticSortArgs = tuple[SortExpression, ...]


class ODManticOrderTranslator(QueryTranslator[SortingQuery, ODManticSortArgs]):
    def __init__(self, model: type[ODManticModel]):
        self._model = model

    def __call__(self, query: SortingQuery) -> ODManticSortArgs:
        return tuple(ODMANTIC_DIRECTION_MAP[entry.direction](getattr(self._model, entry.key)) for entry in query.parsed)

    @classmethod
    def for_model(cls, model: type[ODManticModel]) -> type[Self]:
        # Define the class body as a dictionary
        class_body = {"__init__": lambda self: cls.__init__(self, model=model)}
        # Create the class using the type function
        return type(f"{model.__name__}ODManticOrderTranslator", (cls,), class_body)
