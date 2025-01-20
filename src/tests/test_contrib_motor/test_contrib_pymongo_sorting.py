import pytest

from fast_seeker.contrib.motor.sorting import MotorSorter
from fast_seeker.core.sorting import SortingQuery


@pytest.mark.parametrize(
    "sorting_query, expected",
    [
        pytest.param(SortingQuery(order_by=["-field1"]), [("field1", -1)], id="descending"),
        pytest.param(SortingQuery(order_by=["+field1"]), [("field1", 1)], id="ascending_explicit"),
        pytest.param(SortingQuery(order_by=["field1"]), [("field1", 1)], id="ascending"),
    ],
)
def test_motor_sorter_translate(sorting_query, expected, motor_cursor):
    translated_query = MotorSorter().translate(motor_cursor, sorting_query)
    assert translated_query == expected


@pytest.mark.parametrize(
    "translated_order, expected_expressions",
    [
        pytest.param([("field1", -1)], [("field1", -1)], id="descending"),
        pytest.param([("field1", 1)], [("field1", 1)], id="ascending"),
    ],
)
def test_motor_sorter_execute(translated_order, expected_expressions, motor_cursor):
    cursor = MotorSorter().execute(motor_cursor, translated_order)
    cursor.sort.assert_called_once_with(expected_expressions)
