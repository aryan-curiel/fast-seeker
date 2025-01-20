from unittest.mock import MagicMock, patch

import pytest
from motor.core import AgnosticCollection as Collection
from motor.core import AgnosticCursor as Cursor


@pytest.fixture
def motor_collection():
    mock_collection = MagicMock(spec=Collection)

    mock_collection.find.return_value = MagicMock(spec=Cursor)

    with patch("motor.core.AgnosticCollection", return_value=mock_collection):
        yield mock_collection


@pytest.fixture
def motor_cursor():
    mock_cursor = MagicMock(spec=Cursor)

    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.sort.return_value = mock_cursor

    with patch("motor.core.AgnosticCursor", return_value=mock_cursor):
        yield mock_cursor
