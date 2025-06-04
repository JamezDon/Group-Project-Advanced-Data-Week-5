"""Transform the data ready to upload to s3"""
import os
from os import environ as ENV
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dotenv import load_dotenv


load_dotenv()


def read_csv(table):
    df = pd.read_csv(f"data/{table}.csv")
    return df


def create_directories(base_dir="c17-james-plant-bucket"):
    """Create the directories ready for the metadata"""
    sub_dirs = [
        "input/plant",
        "input/origin",
        "input/country",
        "input/botanist_assignment",
        "input/botanist",
    ]
    for sub_dir in sub_dirs:
        full_path = os.path.join(base_dir, sub_dir)
        os.makedirs(full_path)
        print(f"Created {full_path}")


def get_unique(data):
    unique_data = data.drop_duplicates().reset_index(drop=True)
    return unique_data


def load_metadata():
    tables = ["country", "origin", "plant", "botanist_assignment", "botanist"]
    for table in tables:
        data = read_csv(table)
        unique_data = get_unique(data)
        unique_data.to_parquet(
            f"c17-james-plant-bucket/input/{table}/{table}_metadata.parquet")


if __name__ == "__main__":
    create_directories()
    load_metadata()
