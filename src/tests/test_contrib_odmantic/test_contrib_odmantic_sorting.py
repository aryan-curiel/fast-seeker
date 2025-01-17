import pytest

from fast_seeker.contrib.odmantic.sorting import ODManticOrderTranslator

from .utils import DummyDocument


@pytest.mark.parametrize(
    "order_by, expected",
    [
        (["-field1"], ({"field1": -1},)),
        (["+field1"], ({"field1": 1},)),
        (["field1"], ({"field1": 1},)),
    ],
)
def test_odmantic_sorting_translator(expected, sorting_query):
    translator = ODManticOrderTranslator(DummyDocument)
    translated_query = translator(sorting_query)
    assert translated_query == expected


def test_odmantic_order_translator_ctor__should_assign_model():
    translator = ODManticOrderTranslator(DummyDocument)
    assert translator._model == DummyDocument


def test_odmantic_translator_for_model__should_return_translator():
    translator_class = ODManticOrderTranslator.for_model(DummyDocument)
    assert translator_class.__name__ == "DummyDocumentODManticOrderTranslator"
    assert translator_class()._model == DummyDocument
