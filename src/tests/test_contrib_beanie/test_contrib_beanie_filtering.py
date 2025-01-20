from fast_seeker.contrib.beanie.filtering import BeanieFilterer

from .utils import DummyFindMany


def test_beanie_filterer_default_resolver__should_return_valid_dict():
    filterer = BeanieFilterer()
    translated_args = filterer.default_resolver(None, None, "field", "value")
    assert translated_args == {"field": "value"}


def test_beanie_filterer_execute__should_return_filtered_queryset():
    filterer = BeanieFilterer()
    data = DummyFindMany()
    expressions = [{"field": "value"}]
    result = filterer.execute(data, expressions)
    assert result.find_expressions == expressions
