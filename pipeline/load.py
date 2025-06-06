"""Script for loading data into the SQL Server database."""

from os import environ as ENV
import json

from dotenv import load_dotenv
import pyodbc


def get_db_connection():
    """Gets a connection to the SQL Server plants database."""

    connection = pyodbc.connect(driver=ENV["DB_DRIVER"],
                                server=ENV["DB_HOST"],
                                database=ENV["DB_NAME"],
                                TrustServerCertificate='yes',
                                UID=ENV["DB_USER"],
                                PWD=ENV["DB_PASSWORD"],)

    return connection


def get_db_cursor(connection: "Connection") -> "Cursor":
    """Gets a cursor for the SQL Server plants database."""

    cursor = connection.cursor()

    return cursor


def get_sensor_reading_data(plant: dict) -> dict:
    """Gets the sensor reading data from API data for a single plant."""

    sensor_reading = {}

    sensor_reading["taken_at"] = plant["recording_taken"]
    sensor_reading["temperature"] = plant["temperature"]
    sensor_reading["last_watered"] = plant["last_watered"]
    sensor_reading["soil_moisture"] = plant["soil_moisture"]
    sensor_reading["plant_id"] = plant["plant_id"]

    return sensor_reading


def get_plant_master_data(plant: dict) -> dict:
    """Gets the plant master data from API data."""

    plant_master = {}

    plant_master["plant_name"] = plant["name"]
    plant_master["scientific_name"] = plant.get("scientific_name", None)

    if plant_master["scientific_name"]:
        plant_master["scientific_name"] = "".join(
            plant_master["scientific_name"])

    if "images" in plant:
        if plant["images"] == "null":
            plant.pop("images")

    plant_master["image_link"] = plant.get("images", {}).get("original_url")
    plant_master["soil_moisture"] = plant["soil_moisture"]

    return plant_master


def get_country_id(connection: "Connection", plant: dict) -> dict:
    """Gets the corresponding country ID from database using country name."""

    curs = get_db_cursor(connection)

    curs.execute("SELECT country_id FROM country WHERE country_name = ?",
                 plant["origin_location"]["country"])
    result = curs.fetchone()[0]

    return result


def get_origin_id(connection: "Connection", location_data: dict) -> dict:
    """Gets the corresponding origin ID from database using longitude and latitude."""

    curs = get_db_cursor(connection)

    curs.execute("SELECT country_id FROM origin WHERE longitude = ? AND latitude = ?",
                 (location_data["longitude"], location_data["latitude"]))
    result = curs.fetchone()[0]

    return result


def get_plant_id(connection: "Connection", plant_data: dict) -> dict:
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


def get_botanist_id(connection: "Connection", plant_data: dict) -> dict:
    """Gets the corresponding botanist ID from database using botanist name and email."""

    curs = get_db_cursor(connection)

    curs.execute("""SELECT botanist_id
                    FROM botanist
                    WHERE botanist_name = ?
                    AND email = ?""",
                 (plant_data["botanist"]["name"],
                  plant_data["botanist"]["email"]))
    result = curs.fetchone()[0]

    return result


def load_botanist_assignment_data(connection: "Connection", plants_data: list[dict]) -> None:
    """Loads botanist assignment data from dictionary to botanist assignment table in database."""

    insert_query = """
                IF NOT EXISTS (
                    SELECT 1 FROM botanist_assignment
                    WHERE botanist_id = ?
                    AND plant_id = ?)
                BEGIN
                    INSERT INTO botanist_assignment
                    VALUES (?, ?)
                END
                """

    curs = get_db_cursor(connection)
    for plant in plants_data:
        plant_id = get_plant_id(connection, plant)
        botanist_id = get_botanist_id(connection, plant)
        curs.execute(
            insert_query, (botanist_id,
                           plant_id,
                           botanist_id,
                           plant_id)
        )
        connection.commit()


def load_botanist_data(connection: "Connection", plants_data: list[dict]) -> None:
    """Loads botanist data from dictionary to botanist table in database."""

    insert_query = """
                IF NOT EXISTS (
                    SELECT 1 FROM botanist
                    WHERE botanist_name = ?
                    AND email = ?)
                BEGIN
                    INSERT INTO botanist
                    VALUES (?, ?, ?)
                END
                """

    curs = get_db_cursor(connection)
    for plant in plants_data:
        botanist = plant["botanist"]
        curs.execute(
            insert_query, (botanist["name"],
                           botanist["email"],
                           botanist["name"],
                           botanist["email"],
                           botanist["phone"]))
        connection.commit()


def load_plant_master_data(connection: "Connection", plants_data: list[dict]) -> None:
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


def load_sensor_reading_data(connection: "Connection", plants_data: list[dict]) -> None:
    """Loads sensor reading data from dictionary to sensor reading table in SQL Server database."""

    insert_query = """
                INSERT INTO sensor_reading
                VALUES (?, ?, ?, ?, ?)
                """

    curs = get_db_cursor(connection)
    for plant in plants_data:
        reading = get_sensor_reading_data(plant)
        curs.execute(
            insert_query, (reading["taken_at"],
                           reading["temperature"],
                           reading["last_watered"],
                           reading["soil_moisture"],
                           get_plant_id(connection, plant)))
        connection.commit()


def load_origin_data(connection: "Connection", plants_data: list[dict]) -> None:
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


def load_country_data(connection: "Connection", plants_data: list[dict]) -> None:
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

    seed_data = read_json_data("plant_data.json")

    conn = get_db_connection()

    load_botanist_data(conn, seed_data)
    load_botanist_assignment_data(conn, seed_data)
    load_country_data(conn, seed_data)
    load_origin_data(conn, seed_data)
    load_plant_master_data(conn, seed_data)
    load_sensor_reading_data(conn, seed_data)

    conn.close()
