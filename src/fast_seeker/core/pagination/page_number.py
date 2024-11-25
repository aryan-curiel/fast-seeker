from pydantic import BaseModel, Field

from .base import Paginator


class PageNumberModel(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1)


class PageNumberPaginator[_Data, _Result](Paginator[PageNumberModel, _Data, _Result]): ...
