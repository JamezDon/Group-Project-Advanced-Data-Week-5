# Load data into database

from os import environ as ENV

from dotenv import load_dotenv
import pyodbc
from pyodbc import Connection


def get_db_connection():
    """Gets a connection to the SQL Server plants database."""
    conn = pyodbc.connect(driver='{ODBC Driver 18 for SQL Server}',
                          server=ENV["DB_HOST"],
                          database=ENV["DB_NAME"],
                          TrustServerCertificate='yes',
                          UID=ENV["DB_USER"],
                          PWD=ENV["DB_PASSWORD"],)

    return conn


def get_db_cursor(conn: Connection):
    """Gets a connection to the SQL Server plants database."""

    cursor = conn.cursor()

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

    plant_master["plant_name"] = plant["recording_taken"]
    plant_master["scientific_name"] = plant.get("scientific_name", None)
    plant_master["image_link"] = plant.get("images", None).get("original_url")
    plant_master["soil_moisture"] = plant["soil_moisture"]

    return plant_master


def get_country_id(plant: dict) -> dict:
    """Gets the corresponding country ID from database using country name."""

    curs = get_db_cursor(conn)

    curs.execute("SELECT country_id FROM country_origin WHERE country_name = ?",
                 plant["origin_location"]["country"])
    result = curs.fetchone()[0]

    return result


def load_plant_master_data(plants_data: list[dict]) -> None:
    """Loads plant master data from dictionary to plant table in SQL Server database."""

    insert_query = """
                INSERT INTO plant
                VALUES (?, ?, ?, ?)
                """

    curs = get_db_cursor(conn)
    for plant in plants_data:
        data = get_plant_master_data(plant)
        curs.execute(
            insert_query, (data["plant_name"],
                           data["origin_id"],
                           data["scientific_name"],
                           data["image_link"]))
        conn.commit()


def load_sensor_reading_data(plants_data: list[dict]) -> None:
    """Loads sensor reading data from dictionary to sensor reading table in SQL Server database."""

    insert_query = """
                INSERT INTO sensor_reading
                VALUES (?, ?, ?, ?, ?)
                """

    curs = get_db_cursor(conn)
    for plant in plants_data:
        reading = get_sensor_reading_data(plant)
        curs.execute(
            insert_query, (reading["taken_at"],
                           reading["temperature"],
                           reading["last_watered"],
                           reading["soil_moisture"],
                           reading["plant_id"]))
        conn.commit()


def load_origin_location_data(plants_data: list[dict]) -> None:
    """Loads origin location data from dictionary to origin_location table in SQL Server database."""

    insert_query = """
                INSERT INTO origin_location
                VALUES (?, ?, ?, ?)
                """

    curs = get_db_cursor(conn)
    for plant in plants_data:
        location = plant["origin_location"]
        curs.execute(
            insert_query, (location["latitude"],
                           location["longitude"],
                           location["city"],
                           location["country"]))
        conn.commit()


def load_country_data(plants_data: list[dict]) -> None:
    """Loads country origin data from to country_origin table in SQL Server database."""

    insert_query = """
                IF NOT EXISTS (
                    SELECT 1 FROM country_origin WHERE country_name = ?)
                BEGIN
                    INSERT INTO country_origin VALUES (?)
                END
                """

    curs = get_db_cursor(conn)
    for plant in plants_data:
        country = plant["origin_location"]["country"]
        curs.execute(
            insert_query, (country, country))
        conn.commit()


if __name__ == "__main__":

    load_dotenv()

    mock_data = [
        {
            "plant_id": 1,
            "name": "Venus flytrap",
            "temperature": 14.14,
            "origin_location": {
                "latitude": 43.74,
                "longitude": -11.51,
                "city": "Stammside",
                "country": "Albania"
            },
            "botanist": {
                "name": "Kenneth Buckridge",
                "email": "kenneth.buckridge@lnhm.co.uk",
                "phone": "763.914.8635 x57724"
            },
            "last_watered": "2025-06-03T13:51:41Z",
            "soil_moisture": 95.2,
            "recording_taken": "2025-06-03T15:18:08Z"
        }
    ]

    conn = get_db_connection()
