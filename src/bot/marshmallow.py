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

import settings as stg
from discord.ext import commands

logger = logging.getLogger(__name__)


class MarshmallowBotClient(commands.Bot):
    """Marshmallow Bot Client.

    Subclasses commands.Bot.
    Standardizes bot configuration.
    Handles and loads all cogs via the setup_hook event.
    Handles the on_ready event.
    """

    def __init__(self) -> None:
        """Instantiates Marshmallow Bot Client."""
        super().__init__(
            command_prefix=stg.get_command_prefix(),
            intents=stg.get_intents(),
            activity=stg.get_random_discord_activity(),
        )

        return

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
        return


def main() -> None:
    """Unit Testing."""
    return


if __name__ == "__main__":
    main()
