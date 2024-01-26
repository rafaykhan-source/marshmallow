"""The datahandler module is responsible for writing data and storing data."""

import datetime
import logging
import sys

import pandas as pd
from adt import Person

sys.path.append("..")

logger = logging.getLogger("marshmallow")


def get_assignment_counts(people: list[Person]) -> tuple[int, int]:
    """Returns the assignment counts.

    Args:
        people (list[Person]): The people assigned roles.

    Returns:
        tuple[int, int]: The found and not found counts of people.
    """
    found = 0
    for person in people:
        if person.guild_member:
            found += 1

    return found, len(people) - found


def write_assignment_report(people: list[Person], csv_name: str) -> None:
    """Writes the metrics to a csv file.

    Args:
        people (list[Person]): People Assigned Roles.
        csv_name (str): CSV filename.
    """
    reports = [person.get_metrics() for person in people]

    path = f"assignments/{csv_name}report.csv"
    pd.DataFrame(reports).to_csv(path, index=False)

    logger.info("Wrote '%s' Assignment Report.", csv_name)
    return


def write_daily_message_report(metrics: dict, name: str) -> None:
    """Writes dictionary to csv with name of daily message report.

    Args:
        metrics (dict): metrics for daily messages
        name (str): name of daily message report
    """
    time = datetime.datetime.now().strftime("%m-%d-%Y")  # noqa: DTZ005
    path = f"messages/{name}report-{time}.csv"

    df = pd.DataFrame.from_dict(metrics, orient="index")
    df.columns = [f"date_{i+1}" for i in range(len(df.columns))]
    df = df.rename_axis("display_name (username)").reset_index()
    df.to_csv(path, index=False)

    logger.info("Wrote '%s' Message Report.", name)
    return


def main() -> None:
    """Unit Testing."""
    return


if __name__ == "__main__":
    main()
