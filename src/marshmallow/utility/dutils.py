"""The dutils module contains general discord related utility functions."""

import datetime as dt

import discord
from discord import Color, Embed
from discord.ext import commands


class DateTimeConverter:
    """Converts a string to a datetime."""

    async def convert(self, ctx: commands.Context, s: str) -> dt.datetime:  # noqa
        """Returns datetime from the dt string."""
        return dt.datetime.strptime(s, "%m/%d/%y %I:%M%p").astimezone(dt.UTC)


# TODO: Maybe use factory design pattern?
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


def get_people_embed(members: list[discord.Member]) -> Embed:
    """Returns an embed containing names of provided members.

    Args:
        ctx (commands.Context): The context object.
        members (list[discord.Member]): The members to list.
    """
    embed = get_basic_embed(title="People")

    people = sorted([member.display_name for member in members])
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


def get_failed_assignments_embed(
    people: list,
    assignment_group: str,
) -> Embed:
    """Returns unmatched people embed.

    Args:
        people (list): The list of people.
        assignment_group (str): The assignment group.

    Returns:
        Embed: The failed assignments embed.
    """
    unmatched = [p for p in people if not p.info.found]
    names = [p.info.full_name for p in unmatched]
    aliases = [",".join(p.info.aliases) for p in unmatched]
    roles = [",".join(p.info.role_names) for p in unmatched]

    embed = get_basic_embed(f"Unmatched Person Report: {assignment_group.capitalize()}")
    embed.add_field(
        name="Name:",
        value="\n".join(names),
    )
    embed.add_field(
        name="Aliases:",
        value="\n".join(aliases),
    )
    embed.add_field(
        name="Roles:",
        value="\n".join(roles),
    )
    return embed


if __name__ == "__main__":
    pass
