"""This module represents a portion of the bot relevant to automatic role assignment."""

import logging

import discord
from discord.ext import commands

import marshmallow.settings as stg
from marshmallow.utility.dataproducer import DataServer
from marshmallow.utility.datawriter import DataWriter


class Automation(commands.Cog):
    """A cog for affinity commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        self.logger = logging.getLogger(__name__)
        "The cog's associated logger."
        self.server: DataServer = DataServer()
        "A server for data for the cog."
        self.writer: DataWriter = DataWriter()
        "A writer for data from the cog."

    # TODO: Make this command more generalizable.
    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def create_groups(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.VoiceChannel,
        role: discord.Role,
        channel_base_name: str,
        role_base_name: str,
        start: int,
        end: int,
    ) -> None:
        """Creates groups.

        Args:
            ctx (commands.Context): The command context.
            channel (discord.TextChannel | discord.VoiceChannel): The channel to
                clone from.
            role (discord.Role): The role to clone from.
            channel_base_name (str): The shared base name of the channels.
            role_base_name (str): The shared base name of the roles.
            start (int): The clone range start.
            end (int): The clone range end (exclusive).
        """
        management: commands.Cog = self.bot.get_cog("Management")

        for i in range(start, end):
            channel_name = f"{channel_base_name}{i}"
            role_name = f"{role_base_name}{i}"

            ch = discord.utils.get(ctx.guild.channels, name=channel_name)
            if not ch:
                ch = await management.clone_channel(ctx, channel, channel_name)

            r = discord.utils.get(ctx.guild.roles, name=role_name)
            if not r:
                r = await management.clone_role(ctx, role, role_name)

            await management.grant_channel_access(ctx, r, ch)


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Automation(bot))
