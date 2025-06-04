"""Script for loading master data to database."""

from os import environ as ENV
import json

from dotenv import load_dotenv

from load import get_db_connection, get_db_cursor, get_plant_id, read_json_data


def get_botanist_id(connection, plant_data: dict) -> dict:
    """Gets the corresponding botanist ID from database using botanist name."""

    curs = get_db_cursor(connection)

    curs.execute("""SELECT botanist_id
                    FROM botanist
                    WHERE botanist_name = ?
                    AND email = ?""",
                 (plant_data["botanist"]["name"],
                  plant_data["botanist"]["email"]))
    result = curs.fetchone()[0]

    return result


def load_botanist_assignment_data(connection, plants_data: list[dict]) -> None:
    """Loads botanist assignment data from dictionary to botanist assignment table in database."""

    insert_query = """
                IF NOT EXISTS (
                    SELECT 1 FROM botanist_assignment
                    WHERE botanist_id = ?
                    AND plant_id = ?)
                BEGIN
                    INSERT INTO botanist_assignment
                    VALUES (?, ?)
                END
                """

    curs = get_db_cursor(connection)
    for plant in plants_data:
        plant_id = get_plant_id(connection, plant)
        botanist_id = get_botanist_id(connection, plant)
        curs.execute(
            insert_query, (botanist_id,
                           plant_id,
                           botanist_id,
                           plant_id)
        )
        connection.commit()


def load_botanist_data(connection, plants_data: list[dict]) -> None:
    """Loads botanist data from dictionary to botanist table in database."""

    insert_query = """
                IF NOT EXISTS (
                    SELECT 1 FROM botanist
                    WHERE botanist_name = ?
                    AND email = ?)
                BEGIN
                    INSERT INTO botanist
                    VALUES (?, ?, ?)
                END
                """

    curs = get_db_cursor(connection)
    for plant in plants_data:
        botanist = plant["botanist"]
        curs.execute(
            insert_query, (botanist["name"],
                           botanist["email"],
                           botanist["name"],
                           botanist["email"],
                           botanist["phone"]))
        connection.commit()


if __name__ == "__main__":

    load_dotenv()

    seed_data = read_json_data("plant_data.json")

    conn = get_db_connection()

    load_botanist_data(conn, seed_data)
    load_botanist_assignment_data(conn, seed_data)
