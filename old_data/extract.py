"""Python script to load the hour of data which was more than 24 hours ago"""

import pyodbc
from dotenv import load_dotenv
from os import environ as ENV


def get_connection():
    conn = pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                          f"Server={ENV["DB_HOST"]};"
                          f"Database={ENV["DB_NAME"]};"
                          f"UID={ENV["DB_USER"]};"
                          f"PWD={ENV["DB_PASSWORD"]};"
                          f"Encrypt=no")

    return conn


def get_first_hour():

    SQL_QUERY = ("""
                SELECT * FROM plant;
                """)

    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    record = cursor.fetchall()
    print(record)


if __name__ == "__main__":
    load_dotenv()
    get_connection()
