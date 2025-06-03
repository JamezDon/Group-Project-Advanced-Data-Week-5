# Load data into database

from os import environ as ENV

from dotenv import load_dotenv
from pyodbc import connect, Connection, cursor


def get_db_connection():
    """Gets a connection to the SQL Server plants database."""
    conn = connect(driver='{ODBC Driver 18 for SQL Server}',
                          server=ENV["DB_HOST"],
                          database=ENV["DB_NAME"],
                          TrustServerCertificate='yes',
                          UID=ENV["DB_USER"],
                          PWD=ENV["DB_PASSWORD"],)

    return conn


def get_sensor_reading_data(plant: dict) -> dict:
    """Gets the sensor reading data from API data for a single plant."""
    sensor_reading = {}

    sensor_reading["taken_at"] = plant["recording_taken"]
    sensor_reading["temperature"] = plant["temperature"]
    sensor_reading["last_watered"] = plant["last_watered"]
    sensor_reading["soil_moisture"] = plant["recording_taken"]
    sensor_reading["plant_id"] = plant["plant_id"]

    return sensor_reading


def load_sensor_reading_data(conn: Connection, plants_data: list[dict]) -> None:
    """Loads sensor reading data from dictionary to SQL Server database."""

    insert_query = """
                INSERT INTO sensor_reading
                VALUES (%s, %s, %s, %s, %s)
                """

    with conn.cursor as curs:
        for plant in plants_data:
            reading = get_sensor_reading_data(plant)
            curs.execute(
                insert_query, (reading["taken_at"],
                               reading["temperature"],
                               reading["last_watered"],
                               reading["soil_moisture"],
                               reading["plant_id"]))
            conn.commit()


if __name__ == "__main__":

    load_dotenv()

    conn = get_db_connection()
