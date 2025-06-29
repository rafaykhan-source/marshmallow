"""This module represents the portion of the bot relevant to management.

The commands in this cog pertain to automating the construction
and deletion of roles, channels.
"""

import logging

import discord
from discord.ext import commands

import marshmallow.settings as stg
import marshmallow.utility.dchannels as dch
from marshmallow.utility.dutils import log_send


class Management(commands.Cog):
    """Cog for Server Management Commands.

    Attributes:
        bot (commands.Bot): The bot.
        logger (logging.Logger): The logger.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the Management Cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        self.logger = logging.getLogger(__name__)
        "The cog's associated logger."

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_channels=True)
    async def delete_channels(self, ctx: commands.Context, substring: str) -> None:
        """Deletes all channels with 'substring' in their channel names.

        Args:
            ctx (commands.Context): The command context.
            substring (str): The substring for channel deletion.
        """
        self.logger.info(
            "%s called command 'delete_channels' with substring '%s' in %s.",
            ctx.author.display_name,
            substring,
            ctx.guild.name,
        )
        channels = ctx.guild.channels

        await log_send(
            ctx,
            self.logger,
            f"*Deleting all channels with substring '{substring}.'*",
        )
        for ch in channels:
            if substring in ch.name:
                await ch.delete()
                await log_send(ctx, self.logger, f"Deleted channel '{ch.name}.'")

        await log_send(
            ctx,
            self.logger,
            f"*Deleted all channels with substring '{substring}.'*",
        )

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_channels=True)
    async def delete_category(
        self,
        ctx: commands.Context,
        category: discord.CategoryChannel,
    ) -> None:
        """Deletes the specified category and its channels.

        Args:
            ctx (commands.Context): The command context.
            category (discord.CategoryChannel): The category to delete.
        """
        self.logger.info(
            "%s called command 'delete_category' for '%s' in %s.",
            ctx.author.display_name,
            category.name,
            ctx.guild.name,
        )
        channels = category.channels

        await log_send(
            ctx,
            self.logger,
            f"Deleting Category, *{category.name}*, and subsequent channels.",
        )

        for ch in channels:
            await ch.delete()
            await log_send(ctx, self.logger, f"Deleted channel '{ch.name}'.")

        await category.delete()
        await log_send(ctx, self.logger, f"Deleted category '{category.name}'.")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def delete_roles(self, ctx: commands.Context, substring: str) -> None:
        """Deletes all roles with 'substring' in their role names.

        Args:
            ctx (commands.Context): The command context.
            substring (str): The substring for role deletion.
        """
        self.logger.info(
            "%s called command 'delete_roles' with substring '%s' in %s.",
            ctx.author.display_name,
            substring,
            ctx.guild.name,
        )
        roles = ctx.guild.roles

        await log_send(
            ctx,
            self.logger,
            f"Deleting all roles with base name: *{substring}*",
        )

        for r in roles:
            if substring in r.name:
                await r.delete()
                await log_send(ctx, self.logger, f"Deleted Role: *{r.name}*")

        await log_send(
            ctx,
            self.logger,
            f"Deleted all roles with base name: *{substring}*",
        )

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
        """Clones channels across start to end range (exclusive).

        Args:
            ctx (commands.Context): The command context.
            channel (discord.TextChannel | discord.VoiceChannel): The channel to clone
            from.
            base_name (str): The shared base name of the channels.
            start (int): The clone range start.
            end (int): The clone range end (exclusive).
        """
        self.logger.info(
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
            self.logger,
            f"*Cloning Channels from '{base_name}{start}' to '{base_name}{end}'*",
        )
        channel_names = [f"{base_name}{i}" for i in range(start, end)]
        for name in channel_names:
            await channel.clone(name=name)
            await log_send(ctx, self.logger, f"Cloned channel '{name}.'")
        await log_send(
            ctx,
            self.logger,
            f"*Cloned Channels from '{base_name}{start}' to '{base_name}{end}'*",
        )

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
        self.logger.info(
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

        await log_send(
            ctx,
            self.logger,
            f"*Created new role '{new_role_name}' from '{role.name}.'*",
        )

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
        """Clones roles across start to end range (exclusive).

        Args:
            ctx (commands.Context): The command context.
            role (discord.Role): The role to clone from.
            base_name (str): The shared base name of the roles.
            start (int): The clone range start.
            end (int): The clone range end (exclusive).
        """
        self.logger.info(
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
            self.logger,
            f"*Cloning Roles from '{base_name}{start}' to '{base_name}{end}.'*",
        )
        role_names = [f"{base_name}{i}" for i in range(start, end)]

        for name in role_names:
            await ctx.guild.create_role(
                name=name,
                permissions=role.permissions,
                color=role.color,
            )
            await log_send(ctx, self.logger, f"Cloned role '{name}.'")

        await log_send(
            ctx,
            self.logger,
            f"*Cloned Roles from '{base_name}{start}' to '{base_name}{end}.'*",
        )

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
        if (not ctx.guild) or (not channel) or (not member):
            return

        self.logger.info(
            "%s called command 'grant_channel_access' in %s for %s.",
            ctx.author.display_name,
            channel.name,
            member.name,
        )

        await channel.set_permissions(
            target=member,
            overwrite=dch.get_basic_access_overwrite(channel),
        )

        self.logger.info("Added %s to %s", member.display_name, channel)
        await ctx.send(f"Added {member.display_name} to {channel}.")


async def setup(bot: commands.Bot) -> None:
    """Adds cog to the bot."""
    await bot.add_cog(Management(bot))
