"""Transform the data ready to upload to s3"""
import os
from os import environ as ENV
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dotenv import load_dotenv


load_dotenv()


def read_csv():
    df = pd.read_csv("data/sensor_reading.csv")
    return df


def create_directories(base_dir="c17-james-plant-bucket"):
    """Create the directories ready for the metadata"""
    sub_dirs = [
        "input/plant",
        "input/origin",
        "input/country",
        "input/botanist_assignment",
        "input/botanist",
        "input/plant"
    ]
    for sub_dir in sub_dirs:
        full_path = os.path.join(base_dir, sub_dir)
        os.makedirs(full_path)
        print(f"Created {full_path}")


def get_metadata():
    plant_metadata = data[["plant_id", "plant_name",
                           "origin_id", "scientific_name", "image_link"]].drop_duplicates().reset_index(drop=True)
    country_origin_metadata = data[[
        "country_id", "country_name"]].drop_duplicates().reset_index(drop=True)


def sensor_data(data):
    """Partition data by year, month, day and hour."""
    data["taken_at"] = pd.to_datetime(data["taken_at"])
    data["year"] = data["taken_at"].dt.year
    data["month"] = data["taken_at"].dt.month
    data["day"] = data["taken_at"].dt.day
    data["hour"] = data["taken_at"].dt.hour
    data["minute"] = data["taken_at"].dt.minute
    data = data.drop(columns=["taken_at"])

    table = pa.Table.from_pandas(data)

    pq.write_to_dataset(
        table,
        root_path="c17-james-plant-bucket/input/sensor_reading",
        partition_cols=["year", "month", "day", "hour"]
    )


if __name__ == "__main__":
    sensor_reading_data = read_csv()
    sensor_data(sensor_reading_data)
