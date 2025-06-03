"""Transform the data ready to upload to s3"""
import os


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
    plant_metadata = truck_metadata = data[["truck_id", "truck_name",
                                            "truck_description", "has_card_reader", "fsa_rating"]].drop_duplicates().reset_index(drop=True)


if __name__ == "__main__":
    pass
