import pytest

from fast_seeker.contrib.motor.pagination import (
    MotorLimitOffsetPaginator,
    MotorPageNumberPaginator,
)
from fast_seeker.core.pagination import LimitOffsetQuery, PageNumberQuery


@pytest.mark.parametrize(
    "paginator_class, query, expected_limit, expected_offset",
    [
        pytest.param(MotorLimitOffsetPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="limit_offset"),
        pytest.param(MotorPageNumberPaginator, PageNumberQuery(page=1, size=2), 2, 0, id="page_number"),
    ],
)
def test_motor_paginator_translate__should_return_correct_query(
    paginator_class, query, expected_limit, expected_offset, motor_cursor
):
    paginator = paginator_class()
    result = paginator.translate(motor_cursor, query)
    assert result.limit == expected_limit
    assert result.offset == expected_offset


@pytest.mark.parametrize(
    "paginator_class, query, expected_limit, expected_offset",
    [
        pytest.param(MotorLimitOffsetPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="limit_offset"),
        pytest.param(MotorPageNumberPaginator, LimitOffsetQuery(limit=1, offset=2), 1, 2, id="page_number"),
    ],
)
def test_motor_paginator_execute__should_return_data_with_limit_and_offset(
    paginator_class, query, expected_limit, expected_offset, motor_cursor
):
    paginator_class().execute(motor_cursor, query)
    motor_cursor.limit.assert_called_once_with(expected_limit)
    motor_cursor.skip.assert_called_once_with(expected_offset)
