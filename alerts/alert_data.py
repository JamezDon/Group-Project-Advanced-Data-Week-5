"""Checks the plant data in the RDS for temp or soil moisture outside
the optimum range."""
from os import environ as ENV
from datetime import datetime, timedelta

import pyodbc
from dotenv import load_dotenv


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


def get_last_three_readings(conn) -> list[dict]:
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


def check_recent_alert_sent(plant_id: str, conn) -> bool:
    """Checks if a recent alert was sent for the plant_id provided within the last hour."""

    curs = conn.cursor()
    one_hour_ago = datetime.now() - timedelta(hours=1)

    curs.execute(
        """
    SELECT COUNT(*) FROM alert
    WHERE plant_id = ? AND alert_sent_at >= ?;
    """,
        (plant_id, one_hour_ago)
    )
    recent_alert_count = curs.fetchone()
    curs.close()
    return recent_alert_count != 0


def insert_alert_query(reading: dict, alert_type: list, conn) -> None:
    """Adds an alert into the alert table."""

    curs = conn.cursor()
    plant_id = reading["plant_id"]
    alert_sent_at = datetime.now()
    alert_type = ", ".join(alert_type)

    insert_query = """ INSERT INTO alert 
                        (plant_id, alert_sent_at, alert_type)
                        VALUES (?, ?, ?); """

    curs.execute(insert_query, (plant_id, alert_sent_at, alert_type))

    conn.commit()
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


def check_for_alerts(readings: list[dict], conn) -> list[dict]:
    """Checks if plants require an alert for temp or soil moisture."""

    alert_required = []
    optimum_temp = [15, 30]
    optimum_soil_moisture = 20

    for reading in readings:
        temp = int(reading["avg_temp"])
        soil_moisture = int(
            reading["avg_soil_moisture"])
        temp_alert = not optimum_temp[0] <= temp <= optimum_temp[1]
        soil_moisture_alert = soil_moisture < optimum_soil_moisture

        if temp_alert or soil_moisture_alert:
            recent_alert = check_recent_alert_sent(reading["plant_id"], conn)

            if not recent_alert:
                alert_type = []
                if temp_alert:
                    alert_type.append("temperature")
                if soil_moisture_alert:
                    alert_type.append("soil_moisture")

                insert_alert_query(reading, alert_type, conn)

                alert_required.append(get_alert_record(reading, alert_type))

    return alert_required


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


if __name__ == "__main__":
    load_dotenv()
    database_conn = get_db_connection()
    last_three_readings = get_last_three_readings(database_conn)

    print(database_conn)

    alert_plant_data = check_for_alerts(last_three_readings, database_conn)
