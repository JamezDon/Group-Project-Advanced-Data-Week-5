"""Access the api and retrieve all plant data"""
import json
import logging

import requests

from validate import check_status_code, validate_plant_data


def add_logger():
    """Sets a logger that logs to invalid_plant_data file."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("invalid_plant_data.txt")
    logger.addHandler(file_handler)
    return logger


def save_data_as_json(output):
    """Reads data into a json file."""
    with open(f"plant_data.json", 'w', encoding="utf-8") as file:
        json.dump(output, file, indent=4)


def get_data(id, logger):
    """Retrieve data from api for a given ID."""
    res = requests.get(f"https://sigma-labs-bot.herokuapp.com/api/plants/{id}")
    try:
        check_status_code(res)
        data = res.json()
        return data
    except (ValueError, RuntimeError, PermissionError) as e:
        logger.error(f"Error fetching data: {e}")


def retrieve_all_data(logger):
    """Fetches all plant data from the api for a given range."""
    output_json = []
    for i in range(1, 55):
        plant_data = get_data(i, logger)
        try:
            if validate_plant_data(plant_data):
                logger.error(f"Plant data is invalid: {plant_data}")
            else:
                output_json.append(plant_data)
                save_data_as_json(output_json)
                logger.info("Plant data exported to json file.")
        except ValueError as e:
            logger.error(f"Error when validating plant data: {e}")


if __name__ == "__main__":
    logger = add_logger()
    retrieve_all_data(logger)
