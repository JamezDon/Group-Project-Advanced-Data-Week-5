# Pipeline

## Overview
An ETL pipeline which extracts data from the LNMH plants API, removes any invalid data, then transforms valid data before loading to a **MS SQL Server** database. The database is hosted using **AWS RDS**. 

## Setup and Installation
1. Create and activate a new virtual environment.
    - `python3 -m venv .venv` 
    - `source .venv/bin/activate`
2. Install all dependencies.
    - `pip install -r requirements.txt`
3. If wanting to reset the database to run the pipeline, or to create the necessary tables for the database for the first time:
    - Install the Microsoft SQL Server command-line interface.
        - `brew install sqlcmd`
    - Run the shell script to drop any existing database tables and re-create them.
        - `bash reset.sh`
4. Install the Microsoft ODBC driver for SQL Server allow connection to the database on macOS machines:
    - `brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release`
    - `brew update`
    - `HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18`


# Usage
1. Run the `load.py` script:
    - `python3 load.py`

    - Note: If the other database tables are already populated with master data, this script will simply load relevant data to the `sensor_reading` database table.