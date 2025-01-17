from fast_seeker.core.base import QueryExecutor, QueryProcessor, QueryTranslator


class DummyQueryTranslator(QueryTranslator):
    def __call__(self, query):
        return query


class DummyQueryExecutor(QueryExecutor):
    def __call__(self, data, args):
        return data


def test_query_processor_ctor__should_assign_query_executor_and_query_translator():
    query_translator = DummyQueryTranslator()
    query_executor = DummyQueryExecutor()
    query_processor = QueryProcessor(translator=query_translator, executor=query_executor)
    assert query_processor.translator == query_translator
    assert query_processor.executor == query_executor


def test_query_processor__should_call_translator_and_executor(mocker):
    data, query, result = "data", "query", "result"
    query_processor = QueryProcessor(translator=DummyQueryTranslator(), executor=DummyQueryExecutor())
    result = query_processor(data, query)
    assert result == data
