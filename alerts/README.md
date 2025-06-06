# LMNH Plant Alert System

This module monitors plant sensor readings and triggers alerts when temperature or soil moisture values fall outside optimal ranges. It is designed to be used in an automated pipeline that will run at regular intervals.

The script includes the following steps:
- Connects to a Microsoft SQL Server database.
- Retrieves the last 3 readings for each plant.
- Calculates average temperature and soil moisture.
- Checks if readings fall outside optimal thresholds:
- Temperature: 15°C – 30°C
- Soil Moisture: >= 20%
- Checks if an alert has been sent in the last hour.
- If not, inserts a new alert into the database and creates an alert record.


## Files Explained

alerts/

- `alert_data.py`      
    - Contains the functions for generating an alert record.
- `test_alert_data.py`
    - Contains unit tests for the alert functions.
- `requirements.txt`
    - Contains the required dependencies for the script.
- `.env`
    - Contains the necessary credentials for connecting to the remote database.

Ensure the following environment variables are set via `.env` file:

    DB_HOST
    DB_PORT
    DB_USER
    DB_PASSWORD
    DB_NAME
    DB_SCHEMA

## Setup and installation

- To install dependencies
    - run `pip install -r requirements.txt`
- To run the alert script
    - run `python3 alert_data.py`
- To run tests for the alert functions
    - run `pytest test_alert_data.py`

## Notes:
No alerts will be sent if the readings are within the acceptable range or if an alert was already sent within the past hour.