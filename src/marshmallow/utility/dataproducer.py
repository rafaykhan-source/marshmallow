"""This module represents the data producer for the project.

It is responsible for loading data pertaining to the
marshmallow bot functionality and mapping this data to
custom models.
"""

import csv
import json
import logging
from dataclasses import dataclass, field

from marshmallow.models import GuildPerson, Information


@dataclass
class DataServer:
    """This class is responsible for reading and serving data to Marshmallow."""

    logger: logging.Logger = field(init=False)

    def __post_init__(self) -> None:
        """Acquires logger for the DataServer."""
        self.logger = logging.getLogger(__name__)

    def get_people(self, group: str) -> list[GuildPerson]:
        """Returns the people associated with the group.

        Args:
            group (str): The group to retrieve.

        Returns:
            list[GuildPerson]: The people associated with the group.
        """
        with open(f"../marshmallow-datapipelines/results/{group}.csv") as csv_file:
            self.logger.info("Retrieved People of %s.", group)
            reader = csv.DictReader(csv_file)
            return [
                GuildPerson(
                    Information(
                        full_name=row["full_name"],
                        email=row["email"],
                        role_names=row.get("role_names", "").split(","),
                        aliases=row["aliases"].split(","),
                        affinity_groups=row.get("affinity_groups", "").split(","),
                    ),
                )
                for row in reader
            ]

    def get_report_people(self, group: str) -> list[GuildPerson]:
        """Returns the people associated with the group report.

        Args:
            group (str): The group to retrieve.

        Returns:
            list[GuildPerson]: The people associated with the group report.
        """
        with open(f"assignments/{group}report.csv") as csv_file:
            self.logger.info("Retrieved Assignment Report People of %s.", group)
            reader = csv.DictReader(csv_file)
            return [
                GuildPerson(
                    Information(
                        full_name=row["full_name"],
                        email=row["email"],
                        role_names=row["role_names"].split(","),
                        aliases=row["aliases"].split(","),
                        found=(row["found"] == "True"),
                    ),
                )
                for row in reader
            ]

    def get_welcome_messages(self) -> dict:
        """Returns a mapping of welcome messages.

        Returns:
            dict: The mapping of welcome messages.
        """
        with open(
            "src/marshmallow/settings/resources/welcomes.json",
            encoding="UTF-8",
        ) as data:
            return json.load(data)


if __name__ == "__main__":
    pass
