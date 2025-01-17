import pytest

from fast_seeker.core.sorting import SortingQuery


@pytest.fixture
def sorting_query(order_by):
    return SortingQuery(order_by=order_by)
