from pydantic import BaseModel

from fast_seeker.contrib.basic import DictIterableFilterer, ObjectIterableFilterer


class FilterQuery(BaseModel):
    included_key: str | None = None
    excluded_key: str | None = None


def test_dict_iterable_filterer_filter__should_filter_data():
    filterer = DictIterableFilterer()
    data = [
        {"included_key": "value1", "excluded_key": "value2"},
        {"included_key": "value1", "excluded_key": "value3"},
        {"included_key": "value2", "excluded_key": "value2"},
    ]
    filter_query = FilterQuery(included_key="value1")
    result = filterer.filter(data, filter_query)
    assert list(result) == [
        {"included_key": "value1", "excluded_key": "value2"},
        {"included_key": "value1", "excluded_key": "value3"},
    ]


class Data:
    def __init__(self, included_key, excluded_key):
        self.included_key = included_key
        self.excluded_key = excluded_key


def test_object_iterable_filterer_filter__should_filter_data():
    filterer = ObjectIterableFilterer()

    d1 = Data(included_key="value1", excluded_key="value2")
    d2 = Data(included_key="value1", excluded_key="value3")
    d3 = Data(included_key="value2", excluded_key="value2")

    filter_query = FilterQuery(included_key="value1")
    result = filterer.filter([d1, d2, d3], filter_query)
    assert list(result) == [d1, d2]
