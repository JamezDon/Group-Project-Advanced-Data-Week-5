"""Transform the data ready to upload to s3"""
import os
import pandas as pd


def read_csv():
    df = pd.read_csv("data/plant_data.csv")
    return df


def create_directories(base_dir="c17-james-plants"):
    """Create the directories ready for the metadata"""
    sub_dirs = [
        "input/plant",
        "input/origin_location",
        "input/country_origin",
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


if __name__ == "__main__":
    data = read_csv()
    create_directories()
    get_metadata(data)

    pass
