from abc import ABC, abstractmethod
from typing import TypeVar

_TQuery = TypeVar("_TQuery")
_TArgs = TypeVar("_TArgs")
_TData = TypeVar("_TData")
_TResult = TypeVar("_TResult")


class QueryTranslator[_TQuery, _TArgs](ABC):
    @abstractmethod
    def __call__(self, query: _TQuery) -> _TArgs: ...


class QueryExecutor[_TData, _TArgs, _TResult](ABC):
    @abstractmethod
    def __call__(self, data: _TData, args: _TArgs) -> _TResult: ...


class QueryProcessor[_TData, _TQuery, _TResult, _TArgs](ABC):
    def __call__(self, data: _TData, query: _TQuery) -> _TResult:
        translated_query = self.translate(data, query)
        return self.execute(data, translated_query)

    @abstractmethod
    def translate(self, data: _TData, query: _TQuery) -> _TArgs: ...

    @abstractmethod
    def execute(self, data: _TData, args: _TArgs) -> _TResult: ...
