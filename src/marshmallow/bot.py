"""A class representing a MarshmallowBotClient.

This module defines a class representing Marshmallow bot, which
supports commands/operations relevant for performing/automating
administrative and managerial tasks on the Princeton Emma
Bloomberg Center Discords. The MarshmallowBotClient is a
subclass of discord.py's commands.Bot.

Typical usage example:

  bot = MarshmallowBotClient()
  bot.run(token=TOKEN, log_handler=None)
"""

import logging

from discord.ext import commands

import marshmallow.settings as stg

logger = logging.getLogger(__name__)


class MarshmallowBotClient(commands.Bot):
    """This class contains behavior unique to Marshmallow."""

    def __init__(self) -> None:
        """Instantiates the bot client."""
        super().__init__(
            command_prefix=stg.get_command_prefix(),
            intents=stg.get_intents(),
            activity=stg.get_random_discord_activity(),
        )

    async def setup_hook(self) -> None:
        """Loads bot extensions."""
        cog_names = stg.get_cog_names()

        for cog_name in cog_names:
            await self.load_extension(f"extensions.{cog_name}")
            logger.info("Loaded Cog: %s", cog_name)

        return await super().setup_hook()

    async def on_ready(self) -> None:
        """Event called upon successful login and loaded data."""
        if self.user:
            print(f"Logged in as {self.user} (ID: {self.user.id})")
            logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)


if __name__ == "__main__":
    pass
