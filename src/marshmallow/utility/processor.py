"""The processor module is responsible for processing server information."""

import logging
import re
from collections.abc import Sequence

import discord

from marshmallow.models import GuildPerson

logger = logging.getLogger("assign")


def is_name_match(aliases: list[str], alg_names: list[str]) -> bool:
    """Returns whether there is a match in aliases and alg_names.

    Note that a "match" is really a substring match of alg_name in alias.

    Args:
        aliases (list[str]): Cleaned aliases of an individual (from discord).
        alg_names (list[str]): Cleaned names of an individual (from spreadsheet).

    Returns:
        bool: Presence of a Name Match.
    """
    for alg_name in alg_names:
        for alias in aliases:
            if alg_name in alias:
                return True

    return False


def __clean_name(name: str) -> str:
    """Strips name of whitespace, non-alphabetical characters and makes it lowercase.

    Args:
        name (str): name

    Returns:
        str: cleaned name
    """
    return re.sub(r"[^a-zA-Z]", "", name).lower()


def __clean_aliases(aliases: list[str]) -> list[str]:
    """Returns clean aliases.

    Args:
        aliases (list[str]): unclean aliases

    Returns:
        list[str]: clean aliases
    """
    return [__clean_name(alias) for alias in aliases]


def __get_member_aliases(member: discord.Member) -> list[str]:
    """Returns all clean names/aliases associated with guild member.

    Args:
        member (discord.Member): The Guild Member.

    Returns:
        list[str]: The Member's clean Aliases.
    """
    aliases = set()

    if hasattr(member, "global_name") and member.global_name:
        aliases.add(member.global_name)

    if member.nick:
        aliases.add(member.nick)

    aliases.add(member.name)

    return __clean_aliases(list(aliases))


def create_member_alias_map(
    members: Sequence[discord.Member],
) -> dict[discord.Member, list[str]]:
    """Returns a mapping of members to their clean aliases.

    Args:
        members: The members.

    Returns:
        dict: Mapping of members to aliases.
    """
    return {member: __get_member_aliases(member) for member in members}


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
