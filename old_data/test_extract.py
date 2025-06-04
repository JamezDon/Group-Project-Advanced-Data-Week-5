import pytest
from datetime import datetime, timedelta
from extract import get_time_range


def test_time_range_is_correct():
    """Test that the time range is correct to then delete data"""
    now = datetime.now().replace(
        minute=0, second=0, microsecond=0)
    lower = now - timedelta(hours=25)
    upper = now - timedelta(hours=24)
    assert get_time_range() == (lower, upper)
