from os import environ as ENV
from dotenv import load_dotenv

import pyodbc
from pyodbc import Connection, Cursor


def get_db_connection() -> Connection:
    """Gets a connection to the SQL Server plants database."""

    connection = pyodbc.connect(driver='{ODBC Driver 18 for SQL Server}',
                                server=ENV["DB_HOST"],
                                database=ENV["DB_NAME"],
                                TrustServerCertificate='yes',
                                UID=ENV["DB_USER"],
                                PWD=ENV["DB_PASSWORD"],)

    return connection


def get_db_cursor(connection: Connection) -> Cursor:
    """Gets a cursor for the SQL Server plants database."""

    cursor = connection.cursor()

    return cursor


def get_last_3_readings(conn: Connection) -> list[dict]:
    """Gets the average of the last 3 recorded readings for temperature and soil moisture."""
    query = """WITH ranked_readings as (SELECT 
                    p.plant_id, 
                    p.plant_name, 
                    sr.temperature, 
                    sr.soil_moisture, 
                    sr.taken_at,
                ROW_NUMBER() OVER (PARTITION BY p.plant_id ORDER BY taken_at DESC) AS rank
                FROM plant AS p
                JOIN sensor_reading AS sr
                ON p.plant_id = sr.plant_id)
                SELECT plant_id, plant_name, AVG(temperature), AVG(soil_moisture) from ranked_readings
                  where rank <= 3
                   GROUP BY plant_name, plant_id """
    curs = get_db_cursor(conn)
    curs.execute(query)
    results = curs.fetchall()

    avg_last_3_readings = []
    for result in results:
        avg_last_3_readings.append({
            "plant_id": result[0], "plant_name": result[1],
            "avg_temp": round(float(result[2]), 2),
            "avg_soil_moisture": round(float(result[3]), 2)})

    return avg_last_3_readings


def check_for_temp_alert(readings: list[dict]) -> list[dict]:
    """Checks if the avg temp for the last 3 readings 
    requires an alert to be sent out."""

    alert_required = []
    optimum_temp = list(range(15, 31))
    optimum_soil_moisture = list(range(10, 61))
    for reading in readings:
        if int(reading["avg_temp"]) not in optimum_temp:
            alert_required.append(reading)

    return alert_required


def check_for_soil_moisture_alert(readings: list[dict]) -> list[dict]:
    """Checks if the avg soil moisture for the last 3 readings 
    requires an alert to be sent out."""
    alert_required = []
    optimum_temp = list(range(15, 31))
    optimum_soil_moisture = list(range(10, 61))
    for reading in readings:
        if int(reading["avg_soil_moisture"]) not in optimum_soil_moisture:
            alert_required.append(reading)
    return alert_required


if __name__ == "__main__":
    load_dotenv()
    conn = get_db_connection()
    last_3_readings = get_last_3_readings(conn)
    temp_alerts = check_for_temp_alert(last_3_readings)
    # print(temp_alerts)
    soil_moisture_alerts = check_for_soil_moisture_alert(last_3_readings)
    print(soil_moisture_alerts)
