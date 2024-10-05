"""This module represents the portion of the bot relevant to management.

The commands in this cog pertain to automating the construction
and deletion of roles, channels.
"""

import logging

import discord
import settings as stg
from discord.ext import commands

logger = logging.getLogger("commands")


def generate_names(base_name: str, start: int, end: int) -> list[str]:
    """Generates names from base name across start and end range.

    Args:
        base_name (str): The shared base name.
        start (int): The range start.
        end (int): The range end.

    Returns:
        list[str]: The names across the range.
    """
    return [f"{base_name}{i}" for i in range(start, end)]


async def log_send(ctx: commands.Context, msg: str) -> None:
    """Logs Message and Sends it to the Guild.

    Args:
        ctx (commands.Context): The command context.
        msg (str): Message to log and send.
    """
    logger.info(msg)
    await ctx.send(msg)


class Management(commands.Cog):
    """Cog for Server Management Commands.

    Holds the delete_channels command.
    Holds the delete_roles command.
    Holds the delete_category command.
    Holds the copy_role command.
    Holds the clone_channels command.

    Attributes:
        bot (commands.Bot): The bot.
        logger (logging.Logger): The logger.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the Management Cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_channels=True)
    async def delete_channels(self, ctx: commands.Context, base_name: str) -> None:
        """Deletes all channels with 'base_name' as a substring of the channel name.

        Args:
            ctx (commands.Context): The command context.
            base_name (str): The shared based name of the channels.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'delete_channels' with base name '%s' in %s.",
            ctx.author.display_name,
            base_name,
            ctx.guild.name,
        )
        channels = ctx.guild.channels

        await log_send(ctx, f"Deleting channels with base name: *{base_name}*")
        for ch in channels:
            if base_name in ch.name:
                await ch.delete()
                await log_send(ctx, f"Deleted Channel: *{ch.name}*")

        await log_send(ctx, f"Deleted channels with base name: *{base_name}*")

        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_channels=True)
    async def delete_category(
        self,
        ctx: commands.Context,
        category: discord.CategoryChannel,
    ) -> None:
        """Deletes the specified category and subsequent channels.

        Args:
            ctx (commands.Context): The command context.
            category (discord.CategoryChannel): The category to delete.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'delete_category' for '%s' in %s.",
            ctx.author.display_name,
            category.name,
            ctx.guild.name,
        )
        channels = category.channels

        await log_send(
            ctx,
            f"Deleting Category, *{category.name}*, and subsequent channels.",
        )

        for ch in channels:
            await ch.delete()
            await log_send(ctx, f"Deleted Channel: *{ch.name}*")

        await category.delete()
        await log_send(ctx, f"Deleted Category, *{category.name}*.")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def delete_roles(self, ctx: commands.Context, base_name: str) -> None:
        """Deletes all roles with 'base_name' as a substring of the role name.

        Args:
            ctx (commands.Context): The command context.
            base_name (str): The shared base name of the roles.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'delete_roles' with base name '%s' in %s.",
            ctx.author.display_name,
            base_name,
            ctx.guild.name,
        )
        roles = ctx.guild.roles

        await log_send(ctx, f"Deleting all roles with base name: *{base_name}*")

        for r in roles:
            if base_name in r.name:
                await r.delete()
                await log_send(ctx, f"Deleted Role: *{r.name}*")

        await log_send(ctx, f"Deleted all roles with base name: *{base_name}*")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_channels=True)
    async def clone_channels(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.VoiceChannel,
        base_name: str,
        start: int,
        end: int,
    ) -> None:
        """Clones channels across start to end range (inclusive).

        Args:
            ctx (commands.Context): The command context.
            channel (discord.TextChannel | discord.VoiceChannel): The channel to clone
            from.
            base_name (str): The shared base name of the channels.
            start (int): The clone range start.
            end (int): The clone range end (inclusive).
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'clone_channels' on %s with base name '%s' across %d to %d in %s.",  # noqa: E501
            ctx.author.display_name,
            channel.name,
            base_name,
            start,
            end,
            ctx.guild.name,
        )

        await log_send(
            ctx,
            f"Cloning Channels: *{base_name}{start} -> {end}*",
        )
        channel_names = generate_names(base_name, start, end + 1)

        for name in channel_names:
            await channel.clone(name=name)
            await log_send(ctx, f"Cloned Channel: *{name}*")

        await log_send(ctx, f"Cloned Channels: *{base_name}{start} -> {end}*")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def clone_role(
        self,
        ctx: commands.Context,
        role: discord.Role,
        new_role_name: str,
    ) -> None:
        """Clones specified role giving clone new_role_name.

        Args:
            ctx (commands.Context): The command context.
            role (discord.Role): The role to clone from.
            new_role_name (str): The name of the new role.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'clone_role' on %s in %s.",
            ctx.author.display_name,
            role.name,
            ctx.guild.name,
        )

        await ctx.guild.create_role(
            name=new_role_name,
            permissions=role.permissions,
            color=role.color,
        )

        await log_send(ctx, f"Created new role '{new_role_name}' from {role.name}")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def clone_roles(
        self,
        ctx: commands.Context,
        role: discord.Role,
        base_name: str,
        start: int,
        end: int,
    ) -> None:
        """Clones roles across start to end range (inclusive).

        Args:
            ctx (commands.Context): The command context.
            role (discord.Role): The role to clone from.
            base_name (str): The shared base name of the roles.
            start (int): The clone range start.
            end (int): The clone range end (inclusive).
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'clone_roles' on %s with base name '%s' across %d to %d in %s.",  # noqa: E501
            ctx.author.display_name,
            role.name,
            base_name,
            start,
            end,
            ctx.guild.name,
        )

        await log_send(
            ctx,
            f"Cloning Roles: *{base_name}{start} -> {end}*",
        )
        role_names = generate_names(base_name, start, end + 1)

        for name in role_names:
            await ctx.guild.create_role(
                name=name,
                permissions=role.permissions,
                color=role.color,
            )
            await log_send(ctx, f"Cloned Role: *{name}*")

        await log_send(ctx, f"Cloned Roles: *{base_name}{start} -> {end}*")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def grant_channel_access(
        self,
        ctx: commands.Context,
        member: discord.Member,
        channel: discord.TextChannel | discord.VoiceChannel,
    ) -> None:
        """Grants member basic access to channel.

        Args:
            ctx (commands.Context): The command context.
            member (discord.Member): The member to grant access.
            channel (discord.Channel): The channel to give member access to.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'grant_channel_access' in %s for %s.",
            ctx.author.display_name,
            channel.name,
            member.name,
        )

        overwrite = discord.PermissionOverwrite()
        if isinstance(channel, discord.TextChannel):
            overwrite.send_messages = True
            overwrite.read_messages = True
            overwrite.read_message_history = True
        if isinstance(channel, discord.VoiceChannel):
            overwrite.connect = True
            overwrite.use_soundboard = True
            overwrite.use_voice_activation = True
            overwrite.speak = True
            overwrite.view_channel = True
            overwrite.stream = True
        if member:
            await channel.set_permissions(member, overwrite=overwrite)
            logger.info("Added %s to %s", member.display_name, channel)
            await ctx.send(f"Added {member.display_name} to {channel}")

        return


async def setup(bot: commands.Bot) -> None:
    """Adds cog to the bot."""
    await bot.add_cog(Management(bot))
