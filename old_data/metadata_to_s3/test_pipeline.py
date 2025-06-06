"""Tests for metadata pipeline."""
from unittest.mock import patch, MagicMock
import pytest
import pandas as pd

from transform import get_unique
from extract import get_metadata
from load import connect_to_s3


def test_get_unique_removes_duplicates():
    """Test that the unique function removes all duplicates."""
    df = pd.DataFrame({
        "id": [1,1,2,3,3],
        "value": ["a", "a", "b", "c", "c"]
    })
    result = get_unique(df)
    assert len(result) == 3

