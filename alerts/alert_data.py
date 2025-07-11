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


def recent_alert_sent(plant_id: int, connection: "Connection", alert_type_id: int) -> bool:
    """
    Checks if a recent alert was sent for the 
    plant_id and alert type provided within the last hour.
    """

    curs = connection.cursor()
    one_hour_ago = datetime.now() - timedelta(hours=1)

    curs.execute(
        """
    SELECT COUNT(*) FROM alert
    WHERE plant_id = ? AND sent_at >= ? AND alert_type_id = ?;
    """,
        (plant_id, one_hour_ago, alert_type_id)
    )
    recent_alert_count = curs.fetchone()[0]
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


def temp_alert_required(reading: dict, connection: "Connection") -> bool:
    """Checks if plants require an alert for temp."""

    optimum_temp = [15, 30]

    temp = reading["avg_temp"]

    plant_id = get_plant_id(connection, reading)

    temp_alert = not optimum_temp[0] <= temp <= optimum_temp[1]

    if temp_alert:
        if not recent_alert_sent(
                plant_id, connection, 1):
            return True

    return False


def soil_moisture_alert_required(reading: dict, connection: "Connection") -> bool:
    """Checks if plants require an alert for soil moisture."""

    soil_moisture_threshold = 20

    soil_moisture = reading["avg_soil_moisture"]
    plant_id = get_plant_id(connection, reading)

    soil_moisture_alert = soil_moisture < soil_moisture_threshold

    if soil_moisture_alert:
        if not recent_alert_sent(
                plant_id, connection, 2):
            return True

    return False


def make_html(data: list[dict]) -> str:
    """Converts the data into html to make the alert look better."""
    start = f"""<!DOCTYPE html>
                <html>
                <body>

                <h1> Plant Alerts </h1>
            """
    body = ""
    for plant in data:
        body += f"""
                <h2> Plant {plant["plant_id"]} ({plant["plant_name"]}) </h2>

                <h3> Sensor readings:</h3>
                
                <p> Average temperature over last 3 readings: {plant["avg_temp"]} </p>
                <p> Average soil moisture over last 3 readings: {plant["avg_soil_moisture"]} </p>


                <h3> Alert information:</h3>

                <p> Alert sent at: {plant["alert_sent_at"]} </p>
                <p> Alert type: {plant["alert_type"]} </p>
                """

    end = """</body>
            </html>
            """
    return start+body+end


def add_alert(plant: dict, alert_type: list[str]) -> dict:
    """Adds alerts to the plants that need it."""
    plant["alert_sent_at"] = datetime.now()
    plant["alert_type"] = alert_type
    return plant


if __name__ == "__main__":
    load_dotenv()
    conn = get_db_connection()
    average_readings = get_last_three_readings(conn)
    alerts = []

    for plant in average_readings:
        if temp_alert_required(plant, conn) and soil_moisture_alert_required(plant, conn):
            alerts.append(add_alert(plant, ["temperature", "soil moisture"]))
        elif temp_alert_required(plant, conn):
            insert_alert_query(plant, 1, conn)
            alerts.append(add_alert(plant, ["temperature"]))
        elif soil_moisture_alert_required(plant, conn):
            insert_alert_query(plant, 2, conn)
            alerts.append(add_alert(plant, ["soil moisture"]))

    conn.close()
