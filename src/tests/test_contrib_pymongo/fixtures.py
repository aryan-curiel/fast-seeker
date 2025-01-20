from unittest.mock import MagicMock, patch

import pytest
from pymongo.collection import Collection
from pymongo.cursor import Cursor


@pytest.fixture
def pymongo_collection():
    mock_collection = MagicMock(spec=Collection)

    mock_collection.find.return_value = MagicMock(spec=Cursor)

    with patch("pymongo.collection.Collection", return_value=mock_collection):
        yield mock_collection


@pytest.fixture
def pymongo_cursor():
    mock_cursor = MagicMock(spec=Cursor)

    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.sort.return_value = mock_cursor

    with patch("pymongo.cursor.Cursor", return_value=mock_cursor):
        yield mock_cursor
