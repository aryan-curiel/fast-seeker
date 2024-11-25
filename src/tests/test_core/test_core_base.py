from fast_seeker.core.base import QueryExecutor, QueryProcessor, QueryTranslator


class DummyQueryTranslator(QueryTranslator):
    def __call__(self, *, query, **kwargs):
        return query


class DummyQueryExecutor(QueryExecutor):
    def __call__(self, *, source, translated_query, **kwargs):
        return source


class DummyQueryProcessor(QueryProcessor):
    translator = DummyQueryTranslator()
    executor = DummyQueryExecutor()


def test_query_processor__should_call_translator_and_executor(mocker):
    data, query = "data", "query"
    query_processor = DummyQueryProcessor()
    result = query_processor(source=data, query=query)
    assert result == data
