"""Script that runs the pipeline on a lambda function."""

from dotenv import load_dotenv

from extract import add_logger, retrieve_all_data, load_to_json
from load import read_json_data, get_db_connection, load_origin_data, load_country_data, load_plant_master_data, load_sensor_reading_data


def lambda_handler(event: dict, context: dict) -> dict:
    """Makes a lambda handler."""

    # Extract data
    file_logger = add_logger()
    plant_data = retrieve_all_data(file_logger)
    load_to_json(plant_data)

    # Load data
    load_dotenv()

    seed_data = read_json_data("plant_data.json")

    conn = get_db_connection()

    load_country_data(conn, seed_data)
    load_origin_data(conn, seed_data)
    load_plant_master_data(conn, seed_data)
    load_sensor_reading_data(conn, seed_data)

    conn.close()

    return {None: None}


if __name__ == "__main__":
    print(lambda_handler(None, None))
