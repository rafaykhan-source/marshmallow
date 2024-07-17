"""The dutils module contains general discord related utility functions."""

from datetime import datetime

import discord
from discord import Color, Embed
from discord.ext import commands
from pytz import timezone


class DateTimeConverter:
    """Converts a string to a datetime."""

    async def convert(self, ctx: commands.Context, dt: str) -> datetime:  # noqa
        """Returns datetime from the dt string."""
        return datetime.strptime(dt, "%m/%d/%Y").astimezone(tz=timezone("EST"))


def get_basic_embed(title: str | None = None, description: str | None = None) -> Embed:
    """Returns a basic discord embed.

    Args:
        title (str): The embed title.
        description (str): The embed description.

    Returns:
        Embed: The basic embed template.
    """
    return Embed(
        title=title,
        description=description,
        timestamp=discord.utils.utcnow(),
        color=Color.orange(),
    )


def get_people_embed(members: list[discord.Member]) -> None:
    """Returns an embed containing names of provided members.

    Args:
        ctx (commands.Context): The context object.
        members (list[discord.Member]): The members to list.
    """
    embed = get_basic_embed(title="People")

    people = [member.display_name for member in members]
    embed.add_field(name="Display Names", value="\n".join(people))

    return embed


def get_assignment_summary_embed(
    ctx: commands.Context,
    found: int,
    not_found: int,
) -> Embed:
    """Sends assignment summary to context channel based on assignment stats.

    Args:
        ctx (commands.Context): The command context.
        found (int): The count of people found.
        not_found (int): The count of people not found.
    """
    embed = get_basic_embed(title="Role Assignment Summary")

    embed.add_field(name="People Found:", value=str(found))
    embed.add_field(name="People Not Found:", value=str(not_found))
    if ctx.guild:
        embed.add_field(name="People on Server:", value=str(ctx.guild.member_count))

    return embed
