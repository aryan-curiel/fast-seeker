from fast_seeker.contrib.pymongo.filtering import PyMongoFilterer


def test_pymongo_filterer_default_resolver__should_return_valid_dict():
    filterer = PyMongoFilterer()
    translated_args = filterer.default_resolver(None, None, "field", "value")
    assert translated_args == {"field": "value"}


def test_pymongo_filterer_execute__should_return_filtered_queryset(pymongo_collection):
    filterer = PyMongoFilterer()
    expressions = [{"field": "value"}]
    filterer.execute(pymongo_collection, expressions)
    pymongo_collection.find.assert_called_once_with(*expressions)
