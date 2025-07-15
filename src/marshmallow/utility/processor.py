"""The processor module is responsible for processing server information."""

import logging
from collections.abc import Sequence

import discord

from marshmallow.models import GuildPerson

logger = logging.getLogger("assign")


def is_name_match(guild_names: list[str], aliases: list[str]) -> bool:
    """Returns whether there is a match between an alias and guild name.

    Args:
        guild_names (list[str]): Guild names of an individual (from discord).
        aliases (list[str]): Names of an individual (from spreadsheet).

    Returns:
        bool: Whether a match has occurred.
    """
    for alias in aliases:
        for guild_name in guild_names:
            if alias in guild_name:
                return True

    return False


def _get_guild_member_names(member: discord.Member) -> list[str]:
    """Return all names associated with guild member.

    Args:
        member (discord.Member): The guild member.

    Returns:
        list[str]: Names associated with a guild member.
    """
    names = set()
    names.add(member.name.strip().lower())

    if member.global_name:
        names.add(member.global_name.strip().lower())

    if member.nick:
        names.add(member.nick.strip().lower())

    return list(names)


def get_member_guild_name_map(
    members: Sequence[discord.Member],
) -> dict[discord.Member, list[str]]:
    """Returns a mapping of members to their guild names.

    Args:
        members: The guild members.

    Returns:
        dict: Mapping of members to associated guild names.
    """
    return {member: _get_guild_member_names(member) for member in members}


def get_assignment_counts(people: list[GuildPerson]) -> tuple[int, int]:
    """Returns the assignment counts.

    Args:
        people (list[GuildPerson]): The people assigned roles.

    Returns:
        tuple[int, int]: The found and not found counts of people.
    """
    found = 0
    for person in people:
        if person.guild_member:
            found += 1

    return found, len(people) - found


if __name__ == "__main__":
    pass
