from abc import ABC, abstractmethod
from collections.abc import Callable
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


_QueryTranslator = QueryTranslator[_TQuery, _TArgs] | Callable[[_TQuery], _TArgs]
_QueryExecutor = QueryExecutor[_TData, _TArgs, _TResult] | Callable[[_TData, _TArgs], _TResult]


class QueryProcessor[_TData, _TQuery, _TResult, _TArgs]:
    def __init__(
        self, *, translator: _QueryTranslator[_TQuery, _TArgs], executor: _QueryExecutor[_TData, _TArgs, _TResult]
    ):
        self.translator = translator
        self.executor = executor

    def __call__(self, data: _TData, query: _TQuery) -> _TResult:
        translated_query = self.translator(query)
        return self.executor(data, translated_query)
