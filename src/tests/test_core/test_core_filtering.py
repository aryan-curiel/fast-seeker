import pytest

from fast_seeker.core.filtering import Filterer, FilterModel


def test_filterer__raises_type_error_when_not_implemented():
    class DummyFilterer(Filterer):
        pass

    with pytest.raises(TypeError):
        DummyFilterer()


def test_filterer__raises_not_implemented_error_when_filter_not_implemented():
    class DummyFilterer(Filterer):
        def filter(self, data, filter_query: FilterModel):
            return super().filter(data, filter_query)

    with pytest.raises(NotImplementedError):
        DummyFilterer().filter(None, None)
