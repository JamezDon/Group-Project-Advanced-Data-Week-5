"""Python script to load the hour of data which was more than 24 hours ago."""
from datetime import datetime, timedelta
import os
from os import environ as ENV

import pyodbc
from dotenv import load_dotenv

import pandas as pd


def get_connection():
    """Establish connection to database."""
    conn = pyodbc.connect(f"DRIVER={{{ENV["DB_DRIVER"]}}};"
                          f"Server={ENV["DB_HOST"]};"
                          f"Database={ENV["DB_NAME"]};"
                          f"UID={ENV["DB_USER"]};"
                          f"PWD={ENV["DB_PASSWORD"]};"
                          f"Encrypt=no")

    return conn


def get_time_range() -> tuple[datetime, datetime]:
    """Get time range of the oldest hour of data currently stored in the database."""
    now = datetime.now().replace(
        minute=0, second=0, microsecond=0)
    lower = now - timedelta(hours=25)
    upper = now - timedelta(hours=24)
    return lower, upper


def get_first_hour(lower: datetime, upper: datetime, conn: "Connection") -> dict:
    """Query the database for the oldest hour of data currently stored in the database."""
    print("Getting data")
    query = """
                SELECT * FROM sensor_reading
                WHERE taken_at
                BETWEEN ? AND ?;
                """

    data = pd.read_sql(query, conn, params=(lower,upper))
    print("Got data")
    return data


def delete_first_hour(lower: datetime, upper: datetime, conn: "Connection") -> None:
    """Delete the oldest hour of data currently stored in the database."""
    lower, upper = get_time_range()
    query = """
                DELETE FROM sensor_reading
                WHERE taken_at
                BETWEEN ? AND ?;
                """

    cursor = conn.cursor()
    cursor.execute(query, (lower, upper))


def store_data(data: pd.DataFrame) -> None:
    """Store the hour of data in a csv."""
    if not os.path.exists("data"):
        os.makedirs("data")
    print(data)
    df = pd.DataFrame(data)
    df.to_csv("data/sensor_reading.csv", index=False)


if __name__ == "__main__":
    load_dotenv()
    connection = get_connection()
    lower_bound, upper_bound = get_time_range()
    first_hour = get_first_hour(lower_bound, upper_bound, connection)
    print(first_hour)
    #delete_first_hour(lower_bound, upper_bound, connection)
    store_data(first_hour)
    connection.close()
