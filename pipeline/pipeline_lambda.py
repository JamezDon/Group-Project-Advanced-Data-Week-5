"""Script that runs the pipeline on a lambda function."""

from dotenv import load_dotenv

from extract import add_logger, retrieve_all_data
from load import (get_db_connection, load_origin_data, load_country_data,
                  load_plant_master_data, load_sensor_reading_data)


def lambda_handler(event: dict, context: dict) -> dict:
    """Makes a lambda handler."""

    # Extract data
    file_logger = add_logger()
    plant_data = retrieve_all_data(file_logger)

    # Load data
    conn = get_db_connection()

    load_country_data(conn, plant_data)
    load_origin_data(conn, plant_data)
    load_plant_master_data(conn, plant_data)
    load_sensor_reading_data(conn, plant_data)

    conn.close()

    return {None: None}


if __name__ == "__main__":
    load_dotenv()

    print(lambda_handler(None, None))
