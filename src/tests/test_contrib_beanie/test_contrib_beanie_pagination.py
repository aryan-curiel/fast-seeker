from fast_seeker.contrib.beanie.pagination import BeanieLimitOffsetPaginator, BeaniePageNumberPaginator
from fast_seeker.core.pagination import LimitOffsetModel, PageNumberModel

from .utils import DummyFindMany


def test_beanie_limit_offset_paginator_paginate__should_paginate_data():
    paginator = BeanieLimitOffsetPaginator()
    data = DummyFindMany()
    page_query = LimitOffsetModel(limit=2, offset=1)
    result = paginator.paginate(data, page_query)
    assert result.limit_number == page_query.limit
    assert result.skip_number == page_query.offset


def test_beanie_page_number_paginator_paginate__should_paginate_data():
    paginator = BeaniePageNumberPaginator()
    data = DummyFindMany()
    page_query = PageNumberModel(page=1, size=2)
    result = paginator.paginate(data, page_query)
    assert result.limit_number == page_query.size
    assert result.skip_number == (page_query.page - 1) * page_query.size
