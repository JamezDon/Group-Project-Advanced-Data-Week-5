"""Script that creates a lambda handler for the alert functionality."""

from dotenv import load_dotenv

from alert_data import (get_db_connection, get_last_three_readings,
                        check_for_alerts, make_html)


def lambda_handler(event: dict, context: dict) -> dict:
    """Makes a lambda handler."""

    conn = get_db_connection()
    last_three_readings = get_last_three_readings(conn)
    alerts = check_for_alerts(last_three_readings, conn)
    if alerts:
        html = make_html(alerts)
        return {"status_code": 200,
                "message": html}
    return {None: None}


if __name__ == "__main__":
    load_dotenv()
    print(lambda_handler(None, None))
