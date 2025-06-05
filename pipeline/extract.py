"""Access the api and retrieve all plant data"""
import json
import logging
from logging import Logger

import requests
from joblib import Parallel, delayed

from validate import check_status_code, validate_plant_data, convert_int_to_2dp


def add_logger() -> Logger:
    """Sets a logger that logs to invalid_plant_data file."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    return logger


def load_to_json(output: list[dict]) -> None:
    """Writes validated plant data to json file."""
    with open("plant_data.json", 'w', encoding="utf-8") as file:
        json.dump(output, file, indent=4)


def get_data(plant_id: str, logger: Logger) -> dict:
    """Retrieve data from api for a given ID."""
    res = requests.get(
        f"https://sigma-labs-bot.herokuapp.com/api/plants/{plant_id}", timeout=5)
    try:
        check_status_code(res)
        data = res.json()
        return data
    except (ValueError, RuntimeError, PermissionError) as e:
        logger.error(f"Error fetching data: {e}")


def retrieve_all_data(logger: Logger) -> list[dict]:
    """Fetches all plant data from the api for a given range."""
    output_data = []
    plant_ids = range(1, 54)
    fetched_data = Parallel(n_jobs=10)(
        delayed(get_data)(i, logger) for i in plant_ids)
    logger.info("Plant data fetched from API.")
    for plant_data in fetched_data:
        try:
            if validate_plant_data(plant_data):
                logger.error(f"Plant data is invalid: {plant_data}")
            else:
                converted_data = convert_int_to_2dp(plant_data)
                output_data.append(converted_data)
        except TypeError as e:
            logger.error(f"Error when validating plant data: {e}")
    return output_data


if __name__ == "__main__":
    terminal_logger = add_logger()
    plant_data = retrieve_all_data(terminal_logger)
    # load_to_json(plant_data)
