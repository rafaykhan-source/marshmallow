"""This module represents the portion of the bot relevant to fun and shenanigans.

Containing a cog, the shenanigans module stores a slash command
for handling fun interactions.
"""

import logging

from discord.ext import commands


class Shenanigans(commands.Cog):
    """Cog for Shenanigans.

    Attributes:
        bot (commands.Bot): The bot.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        self.logger = logging.getLogger(__name__)
        "The cog's associated logger."

    @commands.hybrid_command()
    @commands.guild_only()
    async def peep(self, ctx: commands.Context) -> None:
        """Marshmallow responds with peep!

        Args:
            ctx (commands.Context): The command context.
        """
        self.logger.info(
            "%s called command 'peep' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        await ctx.send("peep!")
        self.logger.info("Sent Message: peep!")


async def setup(bot: commands.Bot) -> None:
    """Adds cog to the bot."""
    await bot.add_cog(Shenanigans(bot))
