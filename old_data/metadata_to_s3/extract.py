"""Python script to load the hour of data which was more than 24 hours ago."""
from datetime import datetime, timedelta
import os
from os import environ as ENV

import pyodbc
from dotenv import load_dotenv
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
    now = datetime.now().replace(
        minute=0, second=0, microsecond=0)
    lower = now - timedelta(hours=10)
    upper = now - timedelta(hours=1)
    return lower, upper


def make_query(table: str,lower: datetime,upper: datetime,conn) -> pd.DataFrame:
    """Make select query for given table"""
    print(f"Getting data from {table}")
    query = f"SELECT * FROM {table}; "

    data = pd.read_sql(query, conn)
    return data


def store_data(data: pd.DataFrame, table) -> None:
    """Store the hour of data in a csv"""
    if not os.path.exists("data"):
        os.makedirs("data")
    df = pd.DataFrame(data)
    df.to_csv(f"data/{table}.csv", index=False)


def get_metadata():
    """Main loop for each table in the database."""
    conn = get_connection()
    lower, upper = get_time_range()
    tables = ["country", "origin", "plant", "botanist_assignment", "botanist"]
    for table in tables:
        data = make_query(table,lower,upper,conn)
        store_data(data, table)


if __name__ == "__main__":
    load_dotenv()
    get_metadata()
