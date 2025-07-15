"""A custom subclass of commands.Bot representing Marshmallow."""

import logging

from discord.ext import commands

import marshmallow.settings as stg


class MarshmallowBot(commands.Bot):
    """A subclass of commands.Bot representing Marshmallow."""

    def __init__(self) -> None:
        """Instantiates the bot client."""
        self.logger = logging.getLogger(__name__)
        super().__init__(
            command_prefix=stg.get_command_prefix(),
            intents=stg.get_intents(),
            activity=stg.get_random_discord_activity(),
        )

    async def _load_extensions(self) -> None:
        cogs = stg.get_cogs()

        for cog in cogs:
            await self.load_extension(f"extensions.{cog}")
            self.logger.info("Loaded Cog: %s", cog)

    async def setup_hook(self) -> None:
        """A coroutine to be called to setup the bot."""
        await self._load_extensions()

    async def on_ready(self) -> None:
        """Event called upon successful login and loaded data."""
        if self.user:
            print(f"Logged in as {self.user} (ID: {self.user.id})")
            self.logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)


if __name__ == "__main__":
    pass
