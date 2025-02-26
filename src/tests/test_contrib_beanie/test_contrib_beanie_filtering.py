from fast_seeker.contrib.beanie.filtering import BeanieFilterer, BeanieFilterQueryExecutor, BeanieFilterQueryTranslator

from .utils import DummyFindMany


def test_beanie_filter_query_translator_default_field_translator__should_return_valid_dict():
    translator = BeanieFilterQueryTranslator()
    translated_args = translator._default_field_translator(None, "field", "value")
    assert translated_args == {"field": "value"}


def test_beanie_filter_query_executor__should_return_filtered_queryset():
    executor = BeanieFilterQueryExecutor()
    expressions = [{"field": "value"}]
    result = executor.execute(source=DummyFindMany(), translated_query=expressions)
    assert result.find_expressions == expressions


def test_beanie_filterer__should_have_correct_translator_and_executor():
    filterer = BeanieFilterer()
    assert isinstance(filterer.translator, BeanieFilterQueryTranslator)
    assert isinstance(filterer.executor, BeanieFilterQueryExecutor)
