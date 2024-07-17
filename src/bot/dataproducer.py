"""This module represents the data producer for the project.

It is responsible for loading data pertaining to the
marshmallow bot functionality and mapping this data to
custom ADTs.
"""

import json
import logging

import pandas as pd
from adt import Person

logger = logging.getLogger("utility")


def __create_person(row: list) -> Person:
    return Person(
        full_name=row[0],
        email=row[1],
        role_names=row[2].split(","),
        alg_names=row[3].split(","),
    )


def get_people(assignment_group: str) -> list[Person]:
    """Returns people associated with the assignment group.

    Returns:
        list[Person]: The people in the assignment group.
    """
    data = __get_assignment_group_data(assignment_group)
    logger.info("Retrieved People of %s.", assignment_group)

    return list(map(__create_person, data.values.tolist()))


def __load_data(csv_name: str) -> pd.DataFrame:
    """Returns data from specified csv.

    Returns:
        pd.DataFrame: The data.
    """
    try:
        data = pd.read_csv(csv_name)
        logger.info("Loaded Data From: %s", csv_name)
    except FileNotFoundError:
        logger.error("File Not Found: %s", csv_name)
        data = pd.DataFrame()

    return data


def __create_affinity_person(row: list) -> dict:
    return {
        "full_name": row[0],
        "email": row[1],
        "affinity_groups": row[2].split(","),
        "alg_names": row[3].split(","),
    }


def get_affinity_people() -> list[dict]:
    """Returns affinity group people.

    Returns:
        list[dict]: The affinity group people.
    """
    data = __get_assignment_group_data("affinity")
    return list(map(__create_affinity_person, data.values.tolist()))


def __get_assignment_group_data(assignment_group: str) -> pd.DataFrame:
    """Returns assignment group data for specified assignment group.

    Args:
        assignment_group (str): The assignment group.

    Returns:
        pd.DataFrame: The assignment group's data.
    """
    if not isinstance(assignment_group, str):
        logger.error("Invalid Type for Student Group: %s", type(assignment_group))
        return pd.DataFrame()

    assignment_group = assignment_group.lower()
    return __load_data(f"data/{assignment_group}.csv")


def get_assignment_report(assignment_group: str) -> pd.DataFrame:
    """Returns the assignment report for assignment group.

    Args:
        assignment_group (str): The assignment group.

    Returns:
        pd.DataFrame: The assignment report.
    """
    if not isinstance(assignment_group, str):
        logger.error("Invalid Type for Student Group: %s", type(assignment_group))
        return pd.DataFrame()

    assignment_group = assignment_group.lower()

    return __load_data(f"assignments/{assignment_group}report.csv")


def get_welcome_messages() -> dict:
    """Returns a mapping of welcome messages.

    Returns:
        dict: The mapping of welcome messages.
    """
    with open(
        "src/bot/settings/resources/welcomes.json",
        encoding="UTF-8",
    ) as data:
        return json.load(data)


def main() -> None:
    """Unit Testing."""
    return


if __name__ == "__main__":
    main()
