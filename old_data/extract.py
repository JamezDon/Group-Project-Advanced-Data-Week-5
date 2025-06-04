"""Python script to load the hour of data which was more than 24 hours ago."""
from datetime import datetime, timedelta, timezone
import pyodbc
from dotenv import load_dotenv
import os
from os import environ as ENV
import pandas as pd


def get_connection():
    """Establish connection to database."""
    conn = pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                          f"Server={ENV["DB_HOST"]};"
                          f"Database={ENV["DB_NAME"]};"
                          f"UID={ENV["DB_USER"]};"
                          f"PWD={ENV["DB_PASSWORD"]};"
                          f"Encrypt=no")

    return conn


def get_time_range() -> datetime:
    """Get time range of the oldest hour of data currently stored in the database."""
    # Ensure the time is exactly on the hour
    now = datetime.now().replace(
        minute=0, second=0, microsecond=0)
    lower = now - timedelta(hours=25)
    upper = now - timedelta(hours=24)
    return lower, upper


def get_first_hour(lower: datetime, upper: datetime) -> dict:
    """Query the database for the oldest hour of data currently stored in the database."""
    query = ("""
                SELECT * FROM sensor_reading
                WHERE taken_at
                BETWEEN ? AND ?;
                """)

    cursor = conn.cursor()
    cursor.execute(query, (lower, upper))
    record = cursor.fetchall()
    return record


def delete_first_hour(lower: datetime, upper: datetime) -> None:
    """Delete the oldest hour of data currently stored in the database."""
    lower, upper = get_time_range()
    query = ("""
                DELETE FROM sensor_reading
                WHERE taken_at
                BETWEEN ? AND ?;
                """)

    cursor = conn.cursor()
    cursor.execute(query, (lower, upper))


def store_data(data: pd.DataFrame) -> None:
    """Store the hour of data in a csv"""
    if not os.path.exists("data"):
        os.makedirs("data")
    df = pd.DataFrame(data)
    df.to_csv("data/plant_data.csv", index=False)


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    lower, upper = get_time_range()
    first_hour = get_first_hour(lower, upper)
    print(first_hour)
    delete_first_hour(lower, upper)
    store_data(first_hour)
