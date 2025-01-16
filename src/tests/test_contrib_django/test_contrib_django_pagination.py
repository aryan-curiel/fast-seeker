from django.db.models import QuerySet

from fast_seeker.contrib.django.pagination import QuerySetLimitOffsetPaginator, QuerySetPageNumberPaginator
from fast_seeker.core.pagination import LimitOffsetModel, PageNumberModel


def test_django_limit_offset_paginator_paginate__should_paginate_data(mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)
    paginator = QuerySetLimitOffsetPaginator()
    page_query = LimitOffsetModel(limit=2, offset=1)
    paginator.paginate(mock_queryset, page_query)
    mock_queryset.__getitem__.assert_called_once_with(slice(1, 3))


def test_django_page_number_paginator_paginate__should_paginate_data(mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)
    paginator = QuerySetPageNumberPaginator()
    page_query = PageNumberModel(page=1, size=2)
    paginator.paginate(mock_queryset, page_query)
    mock_queryset.__getitem__.assert_called_once_with(slice(0, 2))
