"""This module is reponsble for writing data to output."""

import csv
import logging
from dataclasses import dataclass, field

from marshmallow.models import GuildPerson


@dataclass
class DataWriter:
    """This class is responsible for writing data to output."""

    logger: logging.Logger = field(init=False)

    def __post_init__(self) -> None:
        """Acquires logger for the DataWriter."""
        self.logger = logging.getLogger(__name__)

    def write_assignment_report(self, people: list[GuildPerson], csv_name: str) -> None:
        """Writes the metrics to a csv file.

        Args:
            people (list[GuildPerson]): The people assigned roles.
            csv_name (str): The name of csv file.
        """
        with open(f"assignments/{csv_name}report.csv", "w") as csv_file:
            fieldnames = [
                "full_name",
                "display_name",
                "username",
                "role_names",
                "email",
                "found",
                "aliases",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for p in people:
                writer.writerow(p.get_metrics())

            self.logger.info("Wrote '%s' Assignment Report.", csv_name)

    def write_message_counts(self, message_counts: dict, csv_name: str) -> None:
        """Writes the message counts to a csv file.

        Args:
            message_counts (dict): The message counts.
            csv_name (str): The name of the csv.
        """
        with open(f"messages/{csv_name}.csv", "w") as f:
            w = csv.writer(f)
            w.writerow(("name", "username", "count"))
            w.writerows([(*person, count) for person, count in message_counts.items()])

        self.logger.info("Wrote '%s' Message Report.", csv_name)


if __name__ == "__main__":
    pass
