from pydantic import BaseModel, Field

from .base import Paginator


class LimitOffsetModel(BaseModel):
    limit: int = Field(20, ge=1)
    offset: int = Field(0, ge=0)


class LimitOffsetPaginator[_Data, _Result](Paginator[LimitOffsetModel, _Data, _Result]): ...
