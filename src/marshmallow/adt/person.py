"""A class consolidating an individual on discord and the spreadsheet.

This module defines the Person ADT, which consolidates the information
between an individual on the spreadsheet and on discord as well as supports
operations for modifying the individual's state on discord.

Typical usage example:

  person = Person()
  person.set_guild_member(member_alias_map)
  person.set_guild_roles(role)

  At this point, person objects are mapped to guild
  members and designated spreadsheet roles.
"""

import logging

import discord
import discord.utils
from discord.ext import commands

import marshmallow.utility.processor as pr

logger = logging.getLogger("assign")


class Person:
    """A Class to Represent a Person.

    Attributes:
        full_name: Person's full name.
        email: Person's email.
        found: Whether person has been mapped to a guild (discord) member.
    """

    def __init__(
        self,
        full_name: str,
        email: str = "",
        role_names: list[str] | None = None,
        alg_names: list[str] | None = None,
    ) -> None:
        """Instantiates a person.

        Args:
            full_name (str): The person's full name.
            email (str, optional): The person's email. Defaults to "".
            role_names (list[str] | None, optional): The person's designated role.
            Defaults to None.
            alg_names (list[str] | None, optional): The person's designated alg_names.
            Defaults to None.
        """
        self.full_name: str = full_name
        "Person's Full Name. Instance Variable."
        self.email: str = email
        "Person's Email. Instance Variable."
        self.role_names: list[str] | None = role_names
        "Names of Person's Designated Roles. Instance Variable."
        self.alg_names: list[str] | None = alg_names
        "Person's Algorithm Names (Used in Name-Matching Algorithm). Instance Variable"
        self.guild_member: discord.Member | None = None
        "Person's Corresponding Guild Member. Instance Variable."
        self.guild_roles: list[discord.Role] | None = None
        "Person's Corresponding Designated Guild Roles. Instance Variable."

    def set_guild_member(
        self,
        members_to_aliases: dict[discord.Member, list[str]],
    ) -> None:
        """Sets person's associated Guild Member.

        Utilizes the name-matching algorithm to set the associated
        guild member. If no match is found, then set to None.

        Args:
            members_to_aliases (dict): Mapping between guild members and their aliases.
        """
        if not isinstance(members_to_aliases, dict):
            logger.error("Argument members_to_aliases is not of type dict.")
            return

        if not self.alg_names:
            logger.info(
                "Cannot set associated guild member when person has no alg_names.",
            )
            return

        for member, aliases in members_to_aliases.items():
            if pr.is_name_match(aliases, self.alg_names):
                self.guild_member = member
                return

        return

    def set_guild_roles(self, override_role: discord.Role | None) -> None:
        """Sets person's designated guild roles based on role_names.

        Args:
            override_role (discord.Role | None): A specific role to assign.
        """
        if not isinstance(override_role, discord.Role | type(None)):
            logger.error("Argument role is not of type discord.Role or NoneType.")
            return

        if not self.guild_member:
            logger.info("Cannot set guild roles for unidentifiable person.")
            return

        self.guild_roles = []

        if override_role:
            self.guild_roles.append(override_role)
            return

        if not self.role_names:
            return

        roles = self.guild_member.guild.roles
        for role_name in self.role_names:
            role = discord.utils.get(roles, name=role_name)
            if role:
                self.guild_roles.append(role)

        return

    def get_display_name(self) -> str | None:
        """Returns the person's display name on discord or None.

        Returns:
            str | None: The person's display name on discord or None.
        """
        return self.guild_member.display_name if self.guild_member else None

    def get_username(self) -> str | None:
        """Returns person's discord username or None if no associated guild member.

        Returns:
            str: The person's discord username or None.
        """
        return self.guild_member.name if self.guild_member else None

    def get_role_names_string(self) -> str:
        """Returns person's designated roles as a single string.

        Returns:
            str: The person's designated roles.
        """
        return ", ".join(self.role_names if self.role_names else [])

    async def assign_roles(self, ctx: commands.Context) -> None:
        """Assigns person's guild member their designated roles if possible.

        Logs the assignment. Sends a message to the context channel.

        Args:
            ctx (commands.Context): The command call context object.
        """
        if not self.guild_member:
            logger.info("%s could not be found on the server.", self.full_name)
            return

        if not self.guild_roles:
            logger.warning("Guild Roles is None.")
            return

        for role in self.guild_roles:
            if role in self.guild_member.roles:
                logger.info("%s already has role %s.", self.full_name, role.name)
            else:
                await self.guild_member.add_roles(role)
                await ctx.send(f"{self.full_name} was newly assigned {role.name}")
                logger.info("%s was newly assigned %s.", self.full_name, role.name)

        return

    def get_metrics(self) -> dict:
        """Returns the metrics associated with a person.

        Returns:
            dict: Person's metrics.
        """
        return {
            "full_name": self.full_name,
            "display_name": self.get_display_name(),
            "username": self.get_username(),
            "discord_roles": self.get_role_names_string(),
            "email": self.email,
            "found": bool(self.guild_member),
        }

    def __str__(self) -> str:
        """Returns a string representation of a Person."""
        return f"""
{self.full_name}
{self.get_display_name()}
{self.email}
{self.role_names}
"""


def main() -> None:
    """Unit Testing."""
    return


if __name__ == "__main__":
    main()
