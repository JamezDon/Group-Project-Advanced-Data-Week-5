"""Script that creates a lambda handler for the alert functionality."""

from dotenv import load_dotenv

from alert_data import (get_db_connection, get_last_three_readings,
                        add_alert, make_html, temp_alert_required,
                        soil_moisture_alert_required, insert_alert_query)


def lambda_handler(event: dict, context: dict) -> dict:
    """Makes a lambda handler."""

    conn = get_db_connection()
    last_three_readings = get_last_three_readings(conn)
    alerts = []
    for plant in last_three_readings:
        if temp_alert_required(plant, conn) and soil_moisture_alert_required(plant, conn):
            alerts.append(add_alert(plant, ["temperature", "soil moisture"]))
        elif temp_alert_required(plant, conn):
            insert_alert_query(plant, 1, conn)
            alerts.append(add_alert(plant, ["temperature"]))
        elif soil_moisture_alert_required(plant, conn):
            insert_alert_query(plant, 2, conn)
            alerts.append(add_alert(plant, ["soil moisture"]))

    if alerts:
        html = make_html(alerts)
        conn.close()
        return {"status_code": 200,
                "message": html}
    conn.close()
    return {None: None}


if __name__ == "__main__":
    load_dotenv()
    print(lambda_handler(None, None))
