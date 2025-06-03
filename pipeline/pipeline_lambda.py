"""Script that runs the pipeline on a lambda function."""

# TODO: Remember to add any imports.
from os import environ as ENV

from dotenv import load_dotenv


def lambda_handler(event: dict, context: dict) -> dict:
    """Makes a lambda handler."""

    # Pull data from API

    # Transform data

    # Load data

    return {None: None}


if __name__ == "__main__":
    load_dotenv()

    lambda_handler()
