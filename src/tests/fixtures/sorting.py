import pytest

from fast_seeker.core.sorting import SortingModel


@pytest.fixture
def sorting_model(order_by):
    return SortingModel(order_by=order_by)
