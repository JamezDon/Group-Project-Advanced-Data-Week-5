"""Checks the plant data in the RDS for temp or soil moisture outside
the optimum range."""
from os import environ as ENV
from datetime import datetime, timedelta

import pyodbc
from dotenv import load_dotenv


def get_db_connection():
    """Gets a connection to the SQL Server plants database."""

    connection = pyodbc.connect(driver=ENV["DB_DRIVER"],
                                server=ENV["DB_HOST"],
                                database=ENV["DB_NAME"],
                                TrustServerCertificate='yes',
                                UID=ENV["DB_USER"],
                                PWD=ENV["DB_PASSWORD"],)

    return connection


def get_db_cursor(connection: "Connection"):
    """Gets a cursor for the SQL Server plants database."""

    cursor = connection.cursor()

    return cursor


def get_last_three_readings(connection: "Connection") -> list[dict]:
    """Gets the average of the last 3 recorded readings for temperature and soil moisture."""
    query = """WITH ranked_readings as 
                (
                SELECT 
                    p.plant_id, 
                    p.plant_name, 
                    sr.temperature, 
                    sr.soil_moisture, 
                    sr.taken_at,
                ROW_NUMBER() OVER (PARTITION BY p.plant_id ORDER BY taken_at DESC) AS rank
                FROM plant AS p
                JOIN sensor_reading AS sr
                ON p.plant_id = sr.plant_id
                )
                SELECT plant_id, plant_name, AVG(temperature), AVG(soil_moisture) 
                FROM ranked_readings
                WHERE rank <= 3
                GROUP BY plant_id, plant_name"""
    curs = get_db_cursor(connection)
    try:
        curs.execute(query)
        results = curs.fetchall()
    finally:
        curs.close()

    avg_last_3_readings = []
    for result in results:
        avg_last_3_readings.append({
            "plant_id": result[0], "plant_name": result[1],
            "avg_temp": round(float(result[2]), 2),
            "avg_soil_moisture": round(float(result[3]), 2)})

    return avg_last_3_readings


def check_recent_alert_sent(plant_id: int, connection: "Connection", alert_type_id: int) -> bool:
    """Checks if a recent alert was sent for the plant_id and alert type provided within the last hour."""

    curs = connection.cursor()
    one_hour_ago = datetime.now() - timedelta(hours=1)

    curs.execute(
        """
    SELECT COUNT(*) FROM alert
    WHERE plant_id = ? AND sent_at >= ? AND alert_type_id = ?;
    """,
        (plant_id, one_hour_ago, alert_type_id)
    )
    recent_alert_count = curs.fetchone()
    curs.close()
    return recent_alert_count != 0


def get_plant_id(connection: "Connection", plant_data: dict) -> dict:
    """Gets the corresponding origin ID from database using longitude and latitude."""

    curs = get_db_cursor(connection)

    curs.execute("""SELECT plant_id
                    FROM plant 
                    WHERE plant_name 
                    COLLATE SQL_Latin1_General_CP1_CS_AS 
                    LIKE ?""",
                 plant_data["plant_name"])
    result = curs.fetchone()[0]

    return result


def insert_alert_query(reading: dict, alert_type_id: int, connection: "Connection") -> None:
    """Adds an alert into the alert table."""

    curs = connection.cursor()
    plant_id = get_plant_id(connection, reading)
    alert_sent_at = datetime.now()

    if alert_type_id == 1:
        alert_value = reading["avg_temp"]
    if alert_type_id == 2:
        alert_value = reading["avg_soil_moisture"]

    insert_query = """ INSERT INTO alert 
                        (plant_id, sent_at, alert_type_id, alert_value)
                        VALUES (?, ?, ?, ?); """

    curs.execute(insert_query, (plant_id, alert_sent_at,
                 alert_type_id, alert_value))

    connection.commit()
    curs.close()


def get_alert_record(reading: dict, alert_type: list) -> dict:
    """Returns a dict of an alert record for the reading provided."""

    now = datetime.now()
    alert_sent_at = datetime.strftime(now, "%Y-%m-%d")

    alert_record = {
        "plant_id": reading["plant_id"],
        "plant_name": reading["plant_name"],
        "avg_temp": reading["avg_temp"],
        "avg_soil_moisture": reading["avg_soil_moisture"],
        "alert_sent_at": alert_sent_at,
        "alert_type": alert_type
    }

    return alert_record


def temp_alert_is_required(reading: dict, connection: "Connection") -> dict | None:
    """Checks if plants require an alert for temp."""

    optimum_temp = [15, 30]

    temp = int(reading["avg_temp"])
    plant_id = get_plant_id(connection, reading)

    temp_alert = not optimum_temp[0] <= temp <= optimum_temp[1]
    print(temp_alert)

    if temp_alert:
        if not check_recent_alert_sent(
                plant_id, connection, 1):
            return True

    return False


def soil_moisture_alert_is_required(reading: dict, connection: "Connection") -> dict | None:
    """Checks if plants require an alert for soil moisture."""

    optimum_soil_moisture = 20

    soil_moisture = int(
        reading["avg_soil_moisture"])
    plant_id = get_plant_id(connection, reading)

    soil_moisture_alert = soil_moisture < optimum_soil_moisture

    if soil_moisture_alert:
        if not check_recent_alert_sent(
                plant_id, connection, 2):
            return True

    return False


if __name__ == "__main__":
    load_dotenv()
    conn = get_db_connection()
    # average_readings = get_last_three_readings(conn)

    average_readings = [{'plant_id': 1, 'plant_name': 'Venus flytrap', 'avg_temp': 14.69, 'avg_soil_moisture': 27.84},
                        {'plant_id': 2, 'plant_name': 'Corpse flower',
                            'avg_temp': 14.21, 'avg_soil_moisture': 30.35},
                        {'plant_id': 3, 'plant_name': 'Rafflesia arnoldii',
                            'avg_temp': 16.37, 'avg_soil_moisture': 26.13},
                        {'plant_id': 4, 'plant_name': 'Black bat flower',
                            'avg_temp': 16.5, 'avg_soil_moisture': 30.18},
                        {'plant_id': 5, 'plant_name': 'Pitcher plant', 'avg_temp': 17.33, 'avg_soil_moisture': 26.9}]

    for plant in average_readings:
        if temp_alert_is_required(plant, conn):
            insert_alert_query(plant, 1, conn)
        if soil_moisture_alert_is_required(plant, conn):
            insert_alert_query(plant, 2, conn)
