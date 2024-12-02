from fast_seeker.contrib.pymongo.pagination import PyMongoLimitOffsetPaginator, PyMongoPageNumberPaginator
from fast_seeker.core.pagination import LimitOffsetModel, PageNumberModel


def test_pymongo_limit_offset_paginator_paginate__should_paginate_data(pymongo_cursor):
    paginator = PyMongoLimitOffsetPaginator()
    page_query = LimitOffsetModel(limit=2, offset=1)
    paginator.paginate(pymongo_cursor, page_query)
    pymongo_cursor.skip.assert_called_once_with(page_query.offset)
    pymongo_cursor.limit.assert_called_once_with(page_query.limit)


def test_pymongo_page_number_paginator_paginate__should_paginate_data(pymongo_cursor):
    paginator = PyMongoPageNumberPaginator()
    page_query = PageNumberModel(page=1, size=2)
    paginator.paginate(pymongo_cursor, page_query)
    pymongo_cursor.skip.assert_called_once_with((page_query.page - 1) * page_query.size)
    pymongo_cursor.limit.assert_called_once_with(page_query.size)
