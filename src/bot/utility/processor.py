"""The processor module is responsible for processing server information."""

import logging
import re
from collections.abc import Sequence

import dataproducer as dp
import discord
import pandas as pd  # noqa: F401
from discord import Embed
from discord.ext import commands

import utility.dutils as du

logger = logging.getLogger("assign")


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


def __get_failed_assignments(assignment_group: str) -> list[str]:
    """Returns people of assignment_group who were not assigned their roles.

    Args:
        assignment_group (str): assignment report

    Returns:
        list[str]: failed assignments for assignment group
    """
    report = dp.get_assignment_report(assignment_group)
    report = report[report["found"] == False]  # noqa

    unmatched = report["full_name"].tolist()
    unmatched.sort()

    return unmatched


def __create_failed_assignments_embed(unmatched: list[str]) -> Embed:
    """Returns unmatched people embed.

    Args:
        unmatched (list[str]): The unmatched people.

    Returns:
        Embed: message
    """
    embed = du.get_basic_embed("Unmatched Person Report")
    embed.add_field(name="People:", value="\n".join(unmatched))

    return embed


async def send_failed_assignments(ctx: commands.Context, assignment_group: str) -> None:
    """Reports Failed Assignments for specified assignment group.

    Args:
        ctx (commands.Context): command calling information
        assignment_group (str): group assigned roles
    """
    unmatched = __get_failed_assignments(assignment_group)
    embed = __create_failed_assignments_embed(unmatched)
    await ctx.send(embed=embed)

    return


def main() -> None:
    """Unit Testing."""
    return


if __name__ == "__main__":
    main()
