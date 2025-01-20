from fast_seeker.core.base import QueryProcessor


class DummyQueryProcessor(QueryProcessor):
    def translate(self, data, query):
        return query

    def execute(self, data, args):
        return data


def test_query_processor__should_call_translator_and_executor(mocker):
    data, query, result = "data", "query", "result"
    query_processor = DummyQueryProcessor()
    result = query_processor(data, query)
    assert result == data
