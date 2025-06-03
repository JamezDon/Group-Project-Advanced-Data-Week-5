"""Tests for validation functions."""

from extract import
from validate import (check_missing_keys, check_missing_location_details,
                      check_missing_botanist_details)


def test_check_missing_keys_returns_list_of_missing_keys_1():
    """Tests that the function returns a list of missing keys 
    if last_watered, soil_moisture and recording_taken keys are missing from plant data. """

    data = {"plant_id": 7, "name": "", "temperature": "",
            "origin_location": "", "botanist": ""}
    assert check_missing_keys(
        data) == ["last_watered", "soil_moisture", "recording_taken"]


def test_check_missing_keys_returns_list_of_missing_keys_2():
    """Tests that the function returns a full list of missing keys 
    if all valid keys are missing from plant data. """

    data = {}
    assert check_missing_keys(
        data) == ["plant_id", "name", "temperature", "origin_location", "botanist",
                  "last_watered", "soil_moisture", "recording_taken"]


def test_check_missing_keys_returns_empty_list_when_no_missing_keys():
    """Tests that the function returns an empty list of missing keys 
    if no top level keys are missing from plant data. """

    data = {"plant_id": "", "name": "", "temperature": "", "origin_location": "", "botanist": "",
            "last_watered": "", "soil_moisture": "", "recording_taken": ""}
    assert check_missing_keys(data) == []


def test_check_missing_location_details_return_list_of_missing_details_1():
    """Tests that the functions returns a list of missing keys when 
    country and city keys are missing from plant data."""

    data = {"origin_location": {"latitude": "", "longitude": ""}}
    assert check_missing_location_details(data) == ["country", "city"]


def test_check_missing_location_details_return_list_of_missing_details_2():
    """Tests that the functions returns a full list of missing keys when 
    all location keys are missing from plant data."""

    data = {"origin_location": {}}
    assert check_missing_location_details(
        data) == ["latitude", "longitude", "country", "city"]


def test_check_missing_location_details_return_empty_list_when_no_missing_details():
    """Tests that the functions returns an empty list of missing keys when 
    no botanist keys are missing from plant data."""

    data = {"origin_location": {"latitude": "",
                                "longitude": "", "country": "", "city": ""}}
    assert check_missing_location_details(
        data) == []
