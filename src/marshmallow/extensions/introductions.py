"""This module represents the portion of the bot relevant to introductions.

Containing a cog, the introductions module stores a slash command
designated for testing the on_member_join event, where those who
join should receive a message encouraging them to change their guild
nickname to their first and last name.
"""

import logging

import discord
from discord.ext import commands

import marshmallow.settings as stg
from marshmallow.settings import Server
from marshmallow.utility.dataproducer import DataServer


class Introductions(commands.Cog):
    """Cog for introductions."""

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the Introductions Cog.

        Args:
            bot (commands.Bot): The bot client.
        """
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        self.logger = logging.getLogger(__name__)
        "The cog's associated logger."
        self.server: DataServer = DataServer()
        "The server of data for the cog."
        self.welcomes: dict = self.server.get_welcome_messages()
        "The program to welcome message mapping."

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """Handles the member guild join event.

        Identifies guild joined and messages member respective guild-specific message.

        Args:
            member (discord.Member): The guild joinee.
        """
        self.logger.info("%s joined %s.", member.display_name, member.guild.name)
        guild_id = member.guild.id

        match guild_id:
            case Server.SIFP:
                await member.send(self.welcomes["sifp"])
            case Server.FSI_ONLINE:
                await member.send(self.welcomes["fsi"])
            case Server.FSI_RESIDENTIAL:
                await member.send(self.welcomes["fsi"])
            case Server.EBCAO_SUMMER:
                await member.send(self.welcomes["ebcao"])
            case Server.MARSHMALLOW_DEV:
                await member.send(self.welcomes["ebcao"])
            case _:
                self.logger.warning(
                    "%s joined unrecognized guild '%s'.",
                    member.display_name,
                    member.guild.name,
                )

        self.logger.info(
            "Sent welcome message to %s for joining '%s'.",
            member.display_name,
            member.guild.name,
        )

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def test_join(self, ctx: commands.Context) -> None:
        """Tests on_member_join event."""
        if not isinstance(ctx.author, discord.Member):
            return

        await self.on_member_join(ctx.author)


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Introductions(bot))
