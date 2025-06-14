"""Tests for validation functions."""


from validate import (get_dict_of_missing_info, check_missing_keys,
                      check_missing_location_details,
                      has_null_images_key, check_negative_moisture)


def test_get_dict_of_missing_info_returns_correct_missing_keys():
    """Tests that the function returns the correct missing keys when 
    given a list of required keys."""

    required_keys = ["name", "plant_id", "origin_location", "soil_moisture"]
    data = {"name": "/", "plant_id": "/"}
    assert get_dict_of_missing_info(data, required_keys) == {"missing_keys": [
        "origin_location", "soil_moisture"]}


def test_get_dict_of_missing_info_returns_correct_missing_values():
    """Tests that the function returns the correct missing values when 
    given a list of required keys."""

    required_keys = ["name", "plant_id", "origin_location", "soil_moisture"]
    data = {"name": "/", "plant_id": "/",
            "origin_location": "", "soil_moisture": ""}
    assert get_dict_of_missing_info(data, required_keys) == {"missing_values": [
        "origin_location", "soil_moisture"]}


def test_get_dict_of_missing_info_returns_correct_missing_keys_and_values():
    """Tests that the function returns the correct missing keys and values when 
    given a list of required keys."""

    required_keys = ["name", "plant_id", "origin_location", "soil_moisture"]
    data = {"name": "/", "origin_location": "", "soil_moisture": ""}
    assert get_dict_of_missing_info(data, required_keys) == {"missing_keys": ["plant_id"],
                                                             "missing_values":
                                                             ["origin_location", "soil_moisture"]}


def test_get_dict_of_missing_info_returns_empty_dict_when_no_missing_keys_and_values():
    """Tests that the function returns an empty list when there are no missing keys when
    given a list of required keys."""

    required_keys = ["name", "plant_id", "origin_location", "soil_moisture"]
    data = {"name": "/", "plant_id": "/",
            "origin_location": "/", "soil_moisture": "/"}
    assert not get_dict_of_missing_info(data, required_keys)


def test_check_missing_keys_returns_dict_of_missing_keys():
    """Tests that the function returns a dict of missing keys 
    if last_watered, soil_moisture and recording_taken keys are missing from plant data. """

    data = {"plant_id": 7, "name": "/", "temperature": "/",
            "origin_location": "/", "botanist": "/"}
    assert check_missing_keys(
        data) == {"missing_keys": ["last_watered", "soil_moisture", "recording_taken"]}


def test_check_missing_keys_returns_dict_of_missing_values():
    """Tests that the function returns a dict of missing values 
    if last_watered, soil_moisture and recording_taken keys have empty values. """

    data = {"plant_id": 7, "name": "/", "temperature": "/",
            "origin_location": "/", "botanist": "/", "last_watered": "", "soil_moisture": "",
            "recording_taken": ""}
    assert check_missing_keys(
        data) == {"missing_values": ["last_watered", "soil_moisture", "recording_taken"]}


def test_check_missing_keys_returns_dict_of_missing_key_and_values():
    """Tests that the function returns a dict of missing keys and missing values
    if plant_id and name keys are missing and last_watered, soil_moisture and 
    recording_taken keys are empty values."""

    data = {"temperature": "/",
            "origin_location": "/", "botanist": "/", "last_watered": "", "soil_moisture": "",
            "recording_taken": ""}
    assert check_missing_keys(
        data) == {"missing_keys": ["plant_id", "name"],
                  "missing_values": ["last_watered", "soil_moisture", "recording_taken"]}


def test_check_missing_keys_returns_empty_dict_if_no_missing_key_and_values():
    """Tests that the function returns an empty dict if no keys and values are missing."""

    data = {"plant_id": "/", "name": "/", "temperature": "/",
            "origin_location": "/", "botanist": "/", "last_watered": "/", "soil_moisture": "/",
            "recording_taken": "/"}
    assert not check_missing_keys(data)


def test_check_missing_location_details_returns_dict_of_missing_keys():
    """Tests that the function returns a dict of missing keys 
    if city and country keys are missing from plant data. """

    data = {"origin_location": {"latitude": 7, "longitude": "/"}}
    assert check_missing_location_details(
        data) == {"missing_keys": ["country", "city"]}


def test_check_missing_location_details_returns_dict_of_missing_values():
    """Tests that the function returns a dict of missing values 
    if city and country keys have empty values."""

    data = {"origin_location": {"latitude": 7,
                                "longitude": "/", "city": "", "country": ""}}
    assert check_missing_location_details(
        data) == {"missing_values": ["country", "city"]}


def test_check_missing_location_details_returns_dict_of_missing_keys_and_values():
    """Tests that the function returns a dict of missing keys and values if 
    latitude key is missing and if city and country keys have empty values."""

    data = {"origin_location": {"longitude": "/", "city": "", "country": ""}}
    assert check_missing_location_details(
        data) == {"missing_keys": ["latitude"], "missing_values": ["country", "city"]}


def test_has_null_images_key_returns_true():
    """Tests that True is returned if images key is present but equals 'null'."""

    assert has_null_images_key({"images": None})


def test_has_null_images_key_returns_false_no_key():
    """Tests that False is returned if images key is not present."""

    data = {"plant_id": 7, "name": "/", "temperature": "/",
            "origin_location": "/", "botanist": "/", "last_watered": "", "soil_moisture": "",
            "recording_taken": ""}

    assert not has_null_images_key({})


def test_has_null_images_key_returns_false_valid_key_nested_dict():
    """Tests that False is returned if images key present and valid."""

    assert not has_null_images_key({"images": {"url": "/"}})


def test_has_negative_soil_moisture():
    """Tests that True is returned when soil moisture is negative"""
    assert check_negative_moisture({"soil_moisture": -12.101})


def test_has_positive_soil_moisture():
    """Tests that False is returned when soil moisture is positive."""
    assert not check_negative_moisture({"soil_moisture": 12.131})


def test_has_zero_moisture():
    """Tests that False is returned when soil moisture is 0."""
    assert not check_negative_moisture({"soil_moisture": 0})


def test_has_negative_small_moisture():
    """Tests that True is returned when soil moisture is -0.001."""
    assert check_negative_moisture({"soil_moisture": -0.001})
