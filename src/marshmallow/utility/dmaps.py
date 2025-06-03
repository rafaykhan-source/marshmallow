"""The dmaps module is responsible for producing and constructing maps for discord objects."""  # noqa: E501

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


async def get_channel_map(
    ctx: commands.Context,
    channels: list[str],
) -> dict[str, discord.abc.GuildChannel]:
    """Returns a map between channel names and their corresponding discord object.

    Args:
        ctx (commands.Context): The command context object.
        channels (list[str]): The desired channels.

    Returns:
        dict[str, discord.GuildChannel]: The channel object mapping.
    """
    channel_map = {}
    for channel in channels:
        guild_channel = await discord.ext.commands.GuildChannelConverter().convert(
            ctx,
            channel,
        )
        if not guild_channel:
            logger.warning("No associated guild channel with %s.", channel)
            print(channel)
        channel_map[channel] = guild_channel

    print([c.name for c in list(channel_map.values())])
    return channel_map


async def get_role_map(
    ctx: commands.Context,
    roles: list[str],
) -> dict[str, discord.Role | None]:
    """Returns a map between role names and their corresponding discord object.

    Args:
        ctx (commands.Context): The command context object.
        roles (list[str]): The desired roles.

    Returns:
        dict[str, discord.GuildChannel]: The role object mapping.
    """
    role_map: dict[str, discord.Role | None] = {}
    for role in roles:
        guild_role = await discord.ext.commands.RoleConverter().convert(ctx, role)
        if not guild_role:
            logger.warning("No associated guild role with %s.", role)
        role_map[role] = guild_role

    return role_map


if __name__ == "__main__":
    pass
