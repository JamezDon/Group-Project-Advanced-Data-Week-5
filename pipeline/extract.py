# Connect to and fetch data from ap

"""Access the api and retrieve all plant data"""
import json
import logging

import requests

from clean import check_plant_found


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


def check_status_code(res, id):
    """Checks the status code of the response."""
    if res.status_code == 404:
        raise ValueError("Plant not found.")
    if res.status_code >= 500:
        raise RuntimeError("Unable to connect to API.")
    if res.status_code == 401:
        raise PermissionError("Invalid API key or not authorised.")
    if res.status_code != 200:
        raise ValueError("Loading weather data was not successful.")


def get_data(id, logger):
    """Retrieve data from api for a given ID."""
    res = requests.get(f"https://sigma-labs-bot.herokuapp.com/api/plants/{id}")
    # check_status_code(res, id)
    data = res.json()
    plant_found = check_plant_found(data)
    if plant_found:
        logger.error(f"{data}")
    else:
        return data


def retrieve_all_data(logger):
    """Fetches all plant data from the api for a given range."""
    output_json = []
    for i in range(1, 51):
        plant_data = get_data(i, logger)
        output_json.append(plant_data)
    save_data_as_json(output_json)


if __name__ == "__main__":
    logger = add_logger()
    retrieve_all_data(logger)
