from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict


class FilterModel(BaseModel):
    model_config = ConfigDict(json_schema_extra={"ignore_none": True})


class Filterer[_Data, _Result](ABC):
    @abstractmethod
    def filter(
        self,
        data: _Data,
        filter_query: FilterModel,
    ) -> _Result:
        raise NotImplementedError
