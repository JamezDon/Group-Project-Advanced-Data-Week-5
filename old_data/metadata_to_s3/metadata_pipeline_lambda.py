"""ETL pipeline to upload all metadata to s3."""
from dotenv import load_dotenv

from extract import get_metadata
from transform import create_directories, load_metadata
from load import connect_to_s3, load_files_to_bucket


def lambda_handler(event: dict, context: dict) -> dict:
    """Run the entire ETL pipeline."""
    #Extract
    get_metadata()

    #Transform
    create_directories()
    load_metadata()

    #Load
    s3_conn = connect_to_s3()
    load_files_to_bucket(s3_conn)

    return {None: None}



if __name__ == "__main__":
    load_dotenv()

    print(lambda_handler(None, None))