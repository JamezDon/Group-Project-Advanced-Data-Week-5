"""Checks the plant data in the RDS for temp or soil moisture outside
the optimum range."""
from os import environ as ENV
from dotenv import load_dotenv

import pyodbc


def get_db_connection():
    """Gets a connection to the SQL Server plants database."""

    connection = pyodbc.connect(driver='{ODBC Driver 18 for SQL Server}',
                                server=ENV["DB_HOST"],
                                database=ENV["DB_NAME"],
                                TrustServerCertificate='yes',
                                UID=ENV["DB_USER"],
                                PWD=ENV["DB_PASSWORD"],)

    return connection


def get_db_cursor(connection):
    """Gets a cursor for the SQL Server plants database."""

    cursor = connection.cursor()

    return cursor


def get_last_3_readings(conn) -> list[dict]:
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


def check_for_alerts(readings: list[dict]) -> list[dict]:
    """Checks if plants require an alert for temp or soil moisture."""

    checked_data = []
    optimum_temp = list(range(15, 31))
    optimum_soil_moisture = list(range(10, 61))

    for reading in readings:
        temp_alert = int(reading["avg_temp"]) not in optimum_temp
        soil_moisture_alert = int(
            reading["avg_soil_moisture"]) not in optimum_soil_moisture
        reading["temp_alert"] = temp_alert
        reading["soil_moisture_alert"] = soil_moisture_alert
        checked_data.append(reading)

    return checked_data


def get_alert_data(potential_alerts: list[dict]) -> list[dict]:
    """Returns a list of plant's which require alerts for temp or soil moisture."""

    alert_required = []
    for reading in potential_alerts:
        if reading["soil_moisture_alert"] or reading["temp_alert"]:
            alert_required.append(reading)
    return alert_required


if __name__ == "__main__":
    load_dotenv()
    database_conn = get_db_connection()
    last_3_readings = get_last_3_readings(database_conn)

    alert_plant_data = check_for_alerts(last_3_readings)
    print(alert_plant_data)
