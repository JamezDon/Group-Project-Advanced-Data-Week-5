"""Test sensor reading pipeline."""
from datetime import datetime, timedelta
import os
import pytest
import tempfile
import shutil

import pandas as pd

from extract import get_time_range
from transform import sensor_data


def test_time_range_is_correct():
    """Test that the time range is correct to then delete data."""
    now = datetime.now().replace(
        minute=0, second=0, microsecond=0)
    lower = now - timedelta(hours=25)
    upper = now - timedelta(hours=24)
    assert get_time_range() == (lower, upper)


def test_sensor_data_grouping_and_aggregation():
    """Test correct average and grouping for temperature"""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["TARGET_BUCKET_NAME"] = tmpdir
    df = pd.DataFrame({
        "plant_id": [1,1,2],
        "taken_at": pd.to_datetime([
            "2024-01-01 10:00:00",
            "2024-01-04 10:00:00",
            "2024-01-02 10:00:00"
        ]),
        "temperature": [20.0, 22.0, 25.0],
        "soil_moisture": [30.0, 32.0, 40.0]
    })
    summary = sensor_data(df)
    assert summary.shape[0] == 3
    assert round(summary["temperature"].iloc[0],1) == 20.0

def test_sensor_data_grouping_and_aggregation_at_same_taken_at():
    """Check correct average and grouping when 2 of the same taken_at"""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["TARGET_BUCKET_NAME"] = tmpdir
    df = pd.DataFrame({
        "plant_id": [1,1,2],
        "taken_at": pd.to_datetime([
            "2024-01-04 10:00:00",
            "2024-01-04 10:00:00",
            "2024-01-07 10:00:00"
        ]),
        "temperature": [20.0, 20.0, 20.0],
        "soil_moisture": [30.0, 32.0, 40.0]
    })
    summary = sensor_data(df)
    assert summary.shape[0] == 2
    assert round(summary["temperature"].iloc[0],1) == 20.0

def test_sensor_data_grouping_and_aggregation_soil_moisture():
    """Check that the soil moisture average is correct"""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["TARGET_BUCKET_NAME"] = tmpdir
    df = pd.DataFrame({
        "plant_id": [1,1,2],
        "taken_at": pd.to_datetime([
            "2024-01-04 10:00:00",
            "2024-01-04 10:00:00",
            "2024-01-07 10:00:00"
        ]),
        "temperature": [20.0, 20.0, 20.0],
        "soil_moisture": [25.0, 25.0, 25.0]
    })
    summary = sensor_data(df)
    assert summary.shape[0] == 2
    assert round(summary["soil_moisture"].iloc[0],1) == 25.0

