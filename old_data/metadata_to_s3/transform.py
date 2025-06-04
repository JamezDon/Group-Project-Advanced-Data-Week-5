"""Transform the data ready to upload to s3"""
import os

import pandas as pd
from dotenv import load_dotenv


load_dotenv()


def read_csv(table: str) -> pd.DataFrame:
    """Read data from given table."""
    df = pd.read_csv(f"data/{table}.csv")
    return df


def create_directories(base_dir="c17-james-plant-bucket"):
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
        os.makedirs(full_path)
        print(f"Created {full_path}")


def get_unique(data: pd.DataFrame) -> pd.DataFrame:
    """Get only unique rows in data"""
    unique_data = data.drop_duplicates().reset_index(drop=True)
    return unique_data


def load_metadata():
    """Main loop to go through each table."""
    tables = ["country", "origin", "plant", "botanist_assignment", "botanist"]
    for table in tables:
        data = read_csv(table)
        unique_data = get_unique(data)
        print(unique_data)
        unique_data.to_parquet(
            f"c17-james-plant-bucket/input/{table}/{table}_metadata.parquet")


if __name__ == "__main__":
    create_directories()
    load_metadata()
