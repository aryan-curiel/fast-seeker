import pytest

from fast_seeker.core.pagination.base import Paginator


def test_paginator__raises_type_error_when_not_implemented():
    class DummyPaginator(Paginator):
        pass

    with pytest.raises(TypeError):
        DummyPaginator()


def test_paginator__raises_not_implemented_error_when_paginate_not_implemented():
    class DummyPaginator(Paginator):
        def paginate(self, data, page_query):
            return super().paginate(data, page_query)

    with pytest.raises(NotImplementedError):
        DummyPaginator().paginate(None, None)
