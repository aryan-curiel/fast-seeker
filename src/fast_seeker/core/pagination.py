from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from .base import QueryProcessor, _TData, _TQuery, _TTranslationResult

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    total: int
    results: list[T]


class LimitOffsetQuery(BaseModel):
    limit: int = Field(20, ge=1)
    offset: int = Field(0, ge=0)


class PageNumberQuery(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1)


class Paginator(
    QueryProcessor[_TQuery, _TTranslationResult, _TData], Generic[_TQuery, _TTranslationResult, _TData]
): ...


class LimitOffsetPaginator(
    Paginator[LimitOffsetQuery, _TTranslationResult, _TData],
    Generic[_TData, _TTranslationResult],
): ...


class PageNumberPaginator(
    Paginator[PageNumberQuery, _TTranslationResult, _TData],
    Generic[_TData, _TTranslationResult],
): ...
