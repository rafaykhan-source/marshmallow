"""A class representing a MarshmallowBotClient."""

import logging

from discord.ext import commands

import marshmallow.settings as stg


class MarshmallowBotClient(commands.Bot):
    """This class contains behavior unique to Marshmallow."""

    def __init__(self) -> None:
        """Instantiates the bot client."""
        super().__init__(
            command_prefix=stg.get_command_prefix(),
            intents=stg.get_intents(),
            activity=stg.get_random_discord_activity(),
        )
        self.logger = logging.getLogger(__name__)

    async def setup_hook(self) -> None:
        """Loads bot extensions."""
        cog_names = stg.get_cog_names()

        for cog_name in cog_names:
            await self.load_extension(f"extensions.{cog_name}")
            self.logger.info("Loaded Cog: %s", cog_name)

        return await super().setup_hook()

    async def on_ready(self) -> None:
        """Event called upon successful login and loaded data."""
        if self.user:
            print(f"Logged in as {self.user} (ID: {self.user.id})")
            self.logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)


if __name__ == "__main__":
    pass
