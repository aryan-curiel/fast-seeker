from pydantic import BaseModel, Field

from fast_seeker.core.base import QueryProcessor


class Page[T](BaseModel):
    total: int
    results: list[T]


class LimitOffsetQuery(BaseModel):
    limit: int = Field(20, ge=1)
    offset: int = Field(0, ge=0)


class LimitOffsetPaginator[_TData, _TResult, _TPageArgs](
    QueryProcessor[_TData, LimitOffsetQuery, _TResult, _TPageArgs]
): ...


class PageNumberQuery(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1)


class PageNumberPaginator[_TData, _TResult, _TPageArgs](
    QueryProcessor[_TData, PageNumberQuery, _TResult, _TPageArgs]
): ...
