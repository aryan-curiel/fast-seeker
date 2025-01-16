from django.db.models import QuerySet

from fast_seeker.contrib.django.sorting import QuerySetSorter
from fast_seeker.core.sorting import SortingModel

########################################
## Tests for the QuerySetSorter class ##
########################################


def test_django_sorter_get_order__should_return_expected_order():
    order_args = ["-key1", "+key2", "key3"]
    sort_query = SortingModel(order_by=order_args)
    order = QuerySetSorter().get_order(sort_query)
    assert order == order_args


def test_django_sorter_apply_sort__should_apply_sorting_in_beanie(mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)

    order = ["-key1", "+key2", "key3"]

    QuerySetSorter()._apply_order(mock_queryset, order)
    mock_queryset.order_by.assert_called_once_with(*order)
