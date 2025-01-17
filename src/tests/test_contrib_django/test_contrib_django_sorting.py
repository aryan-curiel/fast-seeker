import pytest
from django.db.models import QuerySet

from fast_seeker.contrib.django.sorting import QuerySetSorter, django_sorting_executor, django_sorting_translator


@pytest.mark.parametrize(
    "order_by, expected",
    [
        (["-key1"], ["-key1"]),
        (["+key1"], ["+key1"]),
        (["key1"], ["key1"]),
    ],
)
def test_django_sorting_translator(expected, sorting_model):
    translated_query = django_sorting_translator(sorting_model)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        ([("key1", -1)], [("key1", -1)]),
        ([("key1", 1)], [("key1", 1)]),
    ],
)
def test_django_sorting_executor(translated_order, expected_expressions, mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)

    django_sorting_executor(mock_queryset, translated_order)
    mock_queryset.order_by.assert_called_once_with(*expected_expressions)


def test_beanie_sorter_ctor__should_properly_init_sorter():
    sorter = QuerySetSorter()
    assert sorter.translator is not None
    assert sorter.executor is not None
