"""This module is responsible for running Marshmallow."""

import asyncio
import logging
import logging.config

import marshmallow.settings as stg
from marshmallow.bot import MarshmallowBotClient

logger = logging.getLogger("run")


async def main() -> None:
    """Runs Marshmallow."""
    logger.info("Instantiating Marshmallow Bot Client.")
    marsh = MarshmallowBotClient()

    logger.info("Retrieving Token.")

    async with marsh as bot:
        logger.info("Starting Marshmallow.")
        await bot.start(stg.get_token())


asyncio.run(main())
