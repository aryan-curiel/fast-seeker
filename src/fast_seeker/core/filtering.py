from abc import ABC, abstractmethod

from pydantic import BaseModel


class Filterer[_Data, _Result](ABC):
    @abstractmethod
    def filter(
        self,
        data: _Data,
        filter_query: BaseModel,
    ) -> _Result:
        raise NotImplementedError
