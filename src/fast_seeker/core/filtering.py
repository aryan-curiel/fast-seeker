from abc import ABC

from pydantic import BaseModel, ConfigDict

from .base import QueryProcessor


class FilterModel(BaseModel):
    model_config = ConfigDict(json_schema_extra={"ignore_none": True})


class Filterer[_TData, _TResult, _TFilterArgs](QueryProcessor[_TData, FilterModel, _TResult, _TFilterArgs], ABC): ...
