"""Script for loading data into the SQL Server database."""

from os import environ as ENV
import json

from dotenv import load_dotenv
import pyodbc

from extract import retrieve_all_data, add_logger, load_to_json


def get_db_connection():
    """Gets a connection to the SQL Server plants database."""

    connection = pyodbc.connect(driver='{ODBC Driver 18 for SQL Server}',
                                server=ENV["DB_HOST"],
                                database=ENV["DB_NAME"],
                                TrustServerCertificate='yes',
                                UID=ENV["DB_USER"],
                                PWD=ENV["DB_PASSWORD"],)

    return connection


def get_db_cursor(connection):
    """Gets a cursor for the SQL Server plants database."""

    cursor = connection.cursor()

    return cursor


def get_sensor_reading_data(connection, plant: dict) -> dict:
    """Gets the sensor reading data from API data for a single plant."""

    sensor_reading = (plant["recording_taken"],
                      plant["temperature"],
                      plant["last_watered"],
                      plant["soil_moisture"],
                      get_plant_id(connection, plant))

    return sensor_reading


def get_plant_master_data(plant: dict) -> dict:
    """Gets the plant master data from API data."""

    plant_master = {}

    plant_master["plant_name"] = plant["name"]
    plant_master["scientific_name"] = plant.get("scientific_name", None)

    if plant_master["scientific_name"]:
        plant_master["scientific_name"] = "".join(
            plant_master["scientific_name"])

    plant_master["image_link"] = plant.get("images", {}).get("original_url")
    plant_master["soil_moisture"] = plant["soil_moisture"]

    return plant_master


def get_country_id(connection, plant: dict) -> dict:
    """Gets the corresponding country ID from database using country name."""

    curs = get_db_cursor(connection)

    curs.execute("SELECT country_id FROM country WHERE country_name = ?",
                 plant["origin_location"]["country"])
    result = curs.fetchone()[0]

    return result


def get_origin_id(connection, location_data: dict) -> dict:
    """Gets the corresponding origin ID from database using longitude and latitude."""

    curs = get_db_cursor(connection)

    curs.execute("SELECT country_id FROM origin WHERE longitude = ? AND latitude = ?",
                 (location_data["longitude"], location_data["latitude"]))
    result = curs.fetchone()[0]

    return result


def get_plant_id(connection, plant_data: dict) -> dict:
    """Gets the corresponding origin ID from database using longitude and latitude."""

    curs = get_db_cursor(connection)

    curs.execute("""SELECT plant_id
                    FROM plant 
                    WHERE plant_name 
                    COLLATE SQL_Latin1_General_CP1_CS_AS 
                    LIKE ?""",
                 plant_data["name"])
    result = curs.fetchone()[0]

    return result


def load_plant_master_data(connection, plants_data: list[dict]) -> None:
    """Loads plant master data from dictionary to plant table in SQL Server database."""

    insert_query = """
                IF NOT EXISTS (
                    SELECT 1 FROM plant
                    WHERE plant_name = ?
                    AND origin_id = ?)
                BEGIN
                    INSERT INTO plant
                    VALUES (?, ?, ?, ?)
                END
                """

    curs = get_db_cursor(connection)
    for plant in plants_data:
        data = get_plant_master_data(plant)
        origin_id = get_origin_id(connection, plant["origin_location"])

        curs.execute(
            insert_query, (data["plant_name"],
                           origin_id,
                           data["plant_name"],
                           origin_id,
                           data["scientific_name"],
                           data["image_link"]))
        connection.commit()


def load_sensor_reading_data(connection, plants_data: list[dict]) -> None:
    """Loads sensor reading data from dictionary to sensor reading table in SQL Server database."""

    insert_query = """
                INSERT INTO sensor_reading2
                VALUES (?, ?, ?, ?, ?)
                """

    curs = get_db_cursor(connection)

    data_to_insert = []

    curs.fast_executemany = True

    for plant in plants_data:
        data_to_insert.append(get_sensor_reading_data(connection, plant))

    curs.executemany(insert_query, data_to_insert)
    connection.commit()


def load_origin_data(connection, plants_data: list[dict]) -> None:
    """Loads origin location data from dictionary to origin table in database."""

    insert_query = """
                IF NOT EXISTS (
                    SELECT 1 FROM origin
                    WHERE latitude = ?
                    AND longitude = ?)
                BEGIN
                    INSERT INTO origin
                    VALUES (?, ?, ?, ?)
                END
                """

    curs = get_db_cursor(connection)
    for plant in plants_data:
        location = plant["origin_location"]
        curs.execute(
            insert_query, (location["latitude"],
                           location["longitude"],
                           location["latitude"],
                           location["longitude"],
                           location["city"],
                           get_country_id(connection, plant)))
        connection.commit()


def load_country_data(connection, plants_data: list[dict]) -> None:
    """Loads country origin data from to country table in SQL Server database."""

    insert_query = """
                IF NOT EXISTS (
                    SELECT 1
                    FROM country
                    WHERE country_name = ?)
                BEGIN
                    INSERT INTO country VALUES (?)
                END
                """

    curs = get_db_cursor(connection)
    for plant in plants_data:
        country = plant["origin_location"]["country"]
        curs.execute(
            insert_query, (country, country))
        connection.commit()


def read_json_data(filename: str) -> list[dict]:
    """Reads JSON data and returns a list of dictionaries."""

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


if __name__ == "__main__":

    load_dotenv()

    file_logger = add_logger()
    plant_data = retrieve_all_data(file_logger)
    seed_data = load_to_json(plant_data)
    seed_data = read_json_data("plant_data.json")

    conn = get_db_connection()

    load_country_data(conn, seed_data)
    load_origin_data(conn, seed_data)
    load_plant_master_data(conn, seed_data)
    load_sensor_reading_data(conn, seed_data)

    conn.close()
