from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

_TTranslationResult = TypeVar("_TTranslationResult")
_TData = TypeVar("_TData")
_TQuery = TypeVar("_TQuery", bound=BaseModel)


class QueryTranslator(ABC, Generic[_TQuery, _TTranslationResult]):
    @abstractmethod
    def __call__(self, *, query: _TQuery, **kwargs) -> _TTranslationResult: ...


class QueryExecutor(ABC, Generic[_TData, _TTranslationResult]):
    @abstractmethod
    def __call__(self, *, source: _TData, translated_query: _TTranslationResult, **kwargs) -> _TData: ...


class QueryProcessor(ABC, Generic[_TQuery, _TTranslationResult, _TData]):
    translator: QueryTranslator[_TQuery, _TTranslationResult]
    executor: QueryExecutor[_TData, _TTranslationResult]

    def __call__(self, *, source: _TData, query: _TQuery, **kwargs) -> _TData:
        translated_query = self.translator(query=query, **kwargs)
        return self.executor(source=source, translated_query=translated_query, **kwargs)
