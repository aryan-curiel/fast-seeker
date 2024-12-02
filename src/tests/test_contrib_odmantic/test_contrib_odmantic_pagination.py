from fast_seeker.contrib.odmantic.pagination import ODManticLimitOffsetPaginator, ODManticPageNumberPaginator
from fast_seeker.core.pagination import LimitOffsetModel, PageNumberModel


def test_odmantic_limit_offset_paginator_paginate__should_paginate_data():
    paginator = ODManticLimitOffsetPaginator()
    page_query = LimitOffsetModel(limit=2, offset=1)
    result = paginator.paginate(page_query)
    assert result["limit"] == page_query.limit
    assert result["skip"] == page_query.offset


def test_odmantic_page_number_paginator_paginate__should_paginate_data():
    paginator = ODManticPageNumberPaginator()
    page_query = PageNumberModel(page=1, size=2)
    result = paginator.paginate(page_query)
    assert result["limit"] == page_query.size
    assert result["skip"] == (page_query.page - 1) * page_query.size
