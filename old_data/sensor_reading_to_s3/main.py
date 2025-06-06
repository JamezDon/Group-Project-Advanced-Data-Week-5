"""ETL pipeline for uploading live sensor readings to s3."""
from dotenv import load_dotenv

from extract import get_connection, get_time_range, get_first_hour, delete_first_hour,store_data
from transform import read_csv, sensor_data
from load import connect_to_s3, load_files_to_bucket


def main():
    """Loop for the whole ETL pipeline."""
    #Extract
    connection = get_connection()
    lower_bound, upper_bound = get_time_range()
    first_hour = get_first_hour(lower_bound, upper_bound, connection)
    delete_first_hour(lower_bound, upper_bound, connection)
    store_data(first_hour)
    connection.close()

    #Transform
    sensor_reading_data = read_csv()
    sensor_data(sensor_reading_data)

    #Load
    s3_conn = connect_to_s3()
    load_files_to_bucket(s3_conn)

if __name__ == "__main__":
    load_dotenv()
    main()