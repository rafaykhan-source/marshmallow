"""This package maintains the data models for the program."""

import logging
from dataclasses import dataclass, field

import discord
import discord.utils
from discord.ext import commands

import marshmallow.utility.processor as pr


@dataclass(frozen=True)
class Information:
    """This represents the information associated with a person."""

    full_name: str
    email: str
    role_names: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    affinity_groups: list[str] = field(default_factory=list)
    found: bool = False


@dataclass
class GuildPerson:
    """This represents a person matched to a guild member."""

    info: Information
    "The person's information."
    guild_member: discord.Member | None = None
    "The guild member associated with the person."
    logger: logging.Logger = field(init=None)

    def __post_init__(self) -> None:
        """Acquires logger for the GuildPerson."""
        self.logger = logging.getLogger(__name__)

    def set_guild_member(
        self,
        members_to_guild_names: dict[discord.Member, list[str]],
    ) -> None:
        """Sets guild member associated with the person.

        Utilizes the name-matching algorithm to set the associated
        guild member. If no match is found, then set to None.

        Args:
            members_to_guild_names (dict): Mapping from guild members to guild names.
        """
        if not self.info.aliases:
            self.logger.info(
                "Cannot set associated guild member when person has no aliases.",
            )
            return

        for member, guild_names in members_to_guild_names.items():
            if pr.is_name_match(guild_names, self.info.aliases):
                self.guild_member = member
                return

    # TODO: Remove Override Role Logic
    def set_guild_roles(self, override_role: discord.Role | None) -> None:
        """Sets person's designated guild roles based on role_names.

        Args:
            override_role (discord.Role | None): A specific role to assign.
        """
        if not self.guild_member:
            self.logger.info("Cannot set guild roles for unidentifiable person.")
            return

        self.guild_roles = []

        if override_role:
            self.guild_roles.append(override_role)
            return

        if not self.info.role_names:
            return

        roles = self.guild_member.guild.roles
        for role_name in self.info.role_names:
            role = discord.utils.get(roles, name=role_name)
            if role:
                self.guild_roles.append(role)

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

    async def assign_roles(self, ctx: commands.Context) -> None:
        """Assigns person's guild member their designated roles if possible.

        Logs the assignment. Sends a message to the context channel.

        Args:
            ctx (commands.Context): The command call context object.
        """
        if not self.guild_member:
            self.logger.info(
                "%s could not be found on the server.",
                self.info.full_name,
            )
            return

        if not self.guild_roles:
            self.logger.warning("Guild Roles is None.")
            return

        for role in self.guild_roles:
            if role in self.guild_member.roles:
                self.logger.info(
                    "%s already has role %s.",
                    self.info.full_name,
                    role.name,
                )
            else:
                await self.guild_member.add_roles(role)
                await ctx.send(f"{self.info.full_name} was newly assigned {role.name}")
                self.logger.info(
                    "%s was newly assigned %s.",
                    self.info.full_name,
                    role.name,
                )

    def get_metrics(self) -> dict:
        """Returns the metrics associated with a person.

        Returns:
            dict: Person's metrics.
        """
        return {
            "full_name": self.info.full_name,
            "display_name": self.get_display_name(),
            "username": self.get_username(),
            "role_names": ",".join(self.info.role_names),
            "email": self.info.email,
            "found": bool(self.guild_member),
            "aliases": ",".join(self.info.aliases),
        }


if __name__ == "__main__":
    pass
