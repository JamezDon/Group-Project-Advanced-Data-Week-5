"""Transform the data ready to upload to s3."""
import os
from os import environ as ENV

import pandas as pd
from dotenv import load_dotenv


load_dotenv()


def read_csv(table: str) -> pd.DataFrame:
    """Read data from given table."""
    return pd.read_csv(f"data/{table}.csv")


def create_directories(base_dir:str=f"{ENV["TARGET_BUCKET_NAME"]}"):
    """Create the directories ready for the metadata."""
    sub_dirs = [
        "input/plant",
        "input/origin",
        "input/country",
        "input/botanist_assignment",
        "input/botanist",
    ]
    for sub_dir in sub_dirs:
        full_path = os.path.join(base_dir, sub_dir)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created {full_path}")


def get_unique(data: pd.DataFrame) -> pd.DataFrame:
    """Get only unique rows in data."""
    unique_data = data.drop_duplicates().reset_index(drop=True)
    return unique_data


def load_metadata():
    """Main loop to go through each table."""
    tables = ["country", "origin", "plant", "botanist_assignment", "botanist"]
    for table in tables:
        data = read_csv(table)
        unique_data = get_unique(data)
        unique_data.to_parquet(
            f"{ENV["TARGET_BUCKET_NAME"]}/input/{table}/{table}_metadata.parquet")


if __name__ == "__main__":
    load_dotenv()
    create_directories()
    load_metadata()
