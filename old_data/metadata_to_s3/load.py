"""Script to load the summary data to s3."""
import os
from os import environ as ENV

from boto3 import client
from dotenv import load_dotenv


def connect_to_s3() -> client:
    """Connect to s3."""
    s3_client = client(
        "s3", aws_access_key_id=ENV["AWS_ACCESS_KEY_ID"], aws_secret_access_key=ENV[
            "AWS_SECRET_ACCESS_KEY"])
    return s3_client


def load_files_to_bucket(s3: client) -> None:
    """Load to s3."""
    root_path = "c17-james-plant-bucket"
    bucket_name = ENV["TARGET_BUCKET_NAME"]
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith(".parquet"):
                local_path = os.path.join(dirpath, filename)
                s3.upload_file(local_path, bucket_name, local_path)
                print(f"Uploading {local_path} ...")
    print("Upload complete")


if __name__ == "__main__":
    load_dotenv()
    s3_conn = connect_to_s3()
    load_files_to_bucket(s3_conn)
