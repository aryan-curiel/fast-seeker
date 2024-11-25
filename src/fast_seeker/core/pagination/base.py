from abc import ABC, abstractmethod

from pydantic import BaseModel


class Page[T](BaseModel):
    total: int
    results: list[T]


class Paginator[_Query, _Data, _Result](ABC):
    @abstractmethod
    def paginate(self, data: _Data, page_query: _Query) -> _Result:
        raise NotImplementedError
