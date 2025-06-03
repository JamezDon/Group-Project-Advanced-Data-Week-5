# Load data into database

from os import environ as ENV

from dotenv import load_dotenv
import pyodbc


def get_db_connection():
    """Gets a connection to the SQL Server plants database."""
    conn = pyodbc.connect(driver='{ODBC Driver 18 for SQL Server}',
                          server=ENV["DB_HOST"],
                          database=ENV["DB_NAME"],
                          TrustServerCertificate='yes',
                          UID=ENV["DB_USER"],
                          PWD=ENV["DB_PASSWORD"],)

    return conn


if __name__ == "__main__":

    load_dotenv()

    conn = get_db_connection()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLANT")
    output = cursor.fetchall()

    print(output)
