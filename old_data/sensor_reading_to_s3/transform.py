"""Transform the data ready to upload to s3."""
import os
from os import environ as ENV

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dotenv import load_dotenv



def read_csv() -> pd.DataFrame:
    """Read sensor reading csv"""
    return pd.read_csv("data/sensor_reading.csv")


def sensor_data(data: pd.DataFrame):
    """Partition data by year, month, day and hour."""
    data["taken_at"] = pd.to_datetime(data["taken_at"])
    data["year"] = data["taken_at"].dt.year
    data["month"] = data["taken_at"].dt.month
    data["day"] = data["taken_at"].dt.day
    data["hour"] = data["taken_at"].dt.hour
    data["minute"] = data["taken_at"].dt.minute
    data = data.drop(columns=["taken_at"])

    summary = data.groupby(["plant_id", "year", "month", "day", "hour"]
                     ).agg({
                         "temperature": "mean",
                         "soil_moisture": "mean"
                     }).reset_index()


    table = pa.Table.from_pandas(summary)

    pq.write_to_dataset(
        table,
        root_path=f"{ENV["TARGET_BUCKET_NAME"]}/input/sensor_reading",
        partition_cols=["year", "month", "day", "hour"]
    )

    return summary


if __name__ == "__main__":
    load_dotenv()
    sensor_reading_data = read_csv()
    sensor_data(sensor_reading_data)
