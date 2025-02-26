from django.db.models import Q, QuerySet

from fast_seeker.contrib.django.filtering import DjangoFilterer, DjangoFilterQueryExecutor, DjangoFilterQueryTranslator


def test_django_filter_query_translator_default_field_translator__should_return_valid_q_object():
    translator = DjangoFilterQueryTranslator()
    q_object = translator._default_field_translator(None, "field", "value")
    assert q_object == Q(field="value")


def test_django_filter_query_executor__should_return_filtered_queryset(mocker):
    executor = DjangoFilterQueryExecutor()
    mock_queryset = mocker.MagicMock(spec=QuerySet)
    q_object = Q(field="value")
    executor.execute(source=mock_queryset, translated_query=[q_object])
    mock_queryset.filter.assert_called_once_with(q_object)


def test_django_filterer__should_have_correct_translator_and_executor():
    filterer = DjangoFilterer()
    assert isinstance(filterer.translator, DjangoFilterQueryTranslator)
    assert isinstance(filterer.executor, DjangoFilterQueryExecutor)
