"""This module represents the data producer for the project.

It is responsible for loading data pertaining to the
marshmallow bot functionality and mapping this data to
custom models.
"""

import csv
import json
import logging
from dataclasses import dataclass

from marshmallow.models import GuildPerson, Information

logger = logging.getLogger("utility")


@dataclass
class DataServer:
    """This class is responsible for reading and serving data to Marshmallow."""

    def get_people(self, group: str) -> list[GuildPerson]:
        """Returns the people associated with the group.

        Args:
            group (str): The group to retrieve.

        Returns:
            list[GuildPerson]: The people associated with the group.
        """
        with open(f"data/{group}.csv") as csv_file:
            logger.info("Retrieved People of %s.", group)
            reader = csv.DictReader(csv_file)
            return [
                GuildPerson(
                    Information(
                        row["full_name"],
                        row["email"],
                        row["role_names"].split(","),
                        row["alg_names"].split(","),
                    ),
                )
                for row in reader
            ]

    def get_affinity_people(self) -> list[GuildPerson]:
        """Returns affinity group people.

        Returns:
            list[dict]: The affinity group people.
        """
        with open("data/affinity.csv") as csv_file:
            logger.info("Retrieved Affinity People.")
            reader = csv.DictReader(csv_file)
            return [
                GuildPerson(
                    Information(
                        row["full_name"],
                        row["email"],
                        affinity_groups=row["affinity_groups"].split(","),
                        alg_names=row["alg_names"].split(","),
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
