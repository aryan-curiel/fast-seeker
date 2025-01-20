from django.db.models import Q, QuerySet

from fast_seeker.contrib.django.filtering import QuerySetFilterer


def test_query_set_filterer_default_resolver__should_return_valid_q_object():
    filterer = QuerySetFilterer()
    q_object = filterer.default_resolver(None, None, "field", "value")
    assert q_object == Q(field="value")


def test_query_set_filterer_execute__should_return_filtered_queryset(mocker):
    mock_queryset = mocker.MagicMock(spec=QuerySet)
    filterer = QuerySetFilterer()
    q_object = Q(field="value")
    filterer.execute(mock_queryset, [q_object])
    mock_queryset.filter.assert_called_once_with(q_object)
