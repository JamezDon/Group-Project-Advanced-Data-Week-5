"""Python script to load the hour of data which was more than 24 hours ago"""
from datetime import datetime, timedelta
import pyodbc
from dotenv import load_dotenv
import os
from os import environ as ENV
import pandas as pd


def get_connection():
    conn = pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                          f"Server={ENV["DB_HOST"]};"
                          f"Database={ENV["DB_NAME"]};"
                          f"UID={ENV["DB_USER"]};"
                          f"PWD={ENV["DB_PASSWORD"]};"
                          f"Encrypt=no")

    return conn


def get_time_range():
    # 25 hours to account for sometimes the task triggering later
    lower = datetime.now() - timedelta(hours=25)
    upper = datetime.now() - timedelta(hours=23)
    return lower, upper


def get_first_hour(lower, upper):
    query = ("""
                SELECT * FROM sensor_reading
                WHERE taken_at
                BETWEEN ? AND ?;
                """), (lower, upper)

    cursor = conn.cursor()
    cursor.execute(query)
    record = cursor.fetchall()
    print(record)


def delete_first_hour(lower, upper):
    lower, upper = get_time_range()
    query = ("""
                DELETE FROM sensor_reading
                WHERE taken_at
                BETWEEN ? AND ?;
                """), (lower, upper)

    cursor = conn.cursor()
    cursor.execute(query)


def store_data(data):
    os.makedirs("data")
    df = pd.DataFrame(data)
    df.to_csv("data/plant_data.csv", index=False)


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    lower, upper = get_time_range()
    get_first_hour(lower, upper)
    delete_first_hour(lower, upper)
