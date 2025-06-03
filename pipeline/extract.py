"""Access the api and retrieve all plant data"""
import os
import json
import logging

import requests

from validate import check_status_code, validate_plant_data, convert_int_to_2dp


def add_logger():
    """Sets a logger that logs to invalid_plant_data file."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("invalid_plant_data.txt")
    logger.addHandler(file_handler)
    return logger


def load_to_json(filepath, new_reading):
    """Appends new reading to json file."""

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(new_reading)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_data(plant_id, logger):
    """Retrieve data from api for a given ID."""
    res = requests.get(
        f"https://sigma-labs-bot.herokuapp.com/api/plants/{plant_id}", timeout=5)
    try:
        check_status_code(res)
        data = res.json()
        return data
    except (ValueError, RuntimeError, PermissionError) as e:
        logger.error(f"Error fetching data: {e}")


def write_valid_data_to_json(plant_data, logger):
    """Writes valid data to json files."""
    try:
        if validate_plant_data(plant_data):
            logger.error(f"Plant data is invalid: {plant_data}")
        else:
            converted_data = convert_int_to_2dp(plant_data)
            load_to_json("plant_data.json", converted_data)
            logger.info("Plant data exported to json file.")
    except TypeError as e:
        logger.error(f"Error when validating plant data: {e}")


def retrieve_all_data(logger):
    """Fetches all plant data from the api for a given range."""
    for i in range(1, 55):
        plant_data = get_data(i, logger)
        write_valid_data_to_json(plant_data, logger)


if __name__ == "__main__":
    file_logger = add_logger()
    retrieve_all_data(file_logger)
