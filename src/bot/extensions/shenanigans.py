"""This module represents the portion of the bot relevant to fun and shenanigans.

Containing a cog, the shenanigans module stores a slash command
for handling fun interactions.
"""

import logging

from discord.ext import commands

logger = logging.getLogger("commands")


class Shenanigans(commands.Cog):
    """Cog for Shenanigans.

    Attributes:
        bot (commands.Bot): The bot.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the Shenanigans Cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        return

    @commands.hybrid_command()
    @commands.guild_only()
    async def peep(self, ctx: commands.Context) -> None:
        """Marshmallow responds with peep!

        Args:
            ctx (commands.Context): The command context.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'peep' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        await ctx.send("peep!")
        logger.info("Sent Message: peep!")

        return


async def setup(bot: commands.Bot) -> None:
    """Adds cog to the bot."""
    await bot.add_cog(Shenanigans(bot))
    return
