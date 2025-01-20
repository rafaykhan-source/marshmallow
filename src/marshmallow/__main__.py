"""This module is responsible for running Marshmallow."""

import asyncio
import logging
import logging.config

import marshmallow.settings as stg
from marshmallow.bot import MarshmallowBotClient


async def main() -> None:
    """Runs Marshmallow."""
    logger = logging.getLogger("run")

    logger.info("Instantiating Marshmallow Bot Client.")
    marsh = MarshmallowBotClient()

    logger.info("Retrieving Token.")
    token = stg.get_token()

    async with marsh as bot:
        logger.info("Starting Marshmallow.")
        await bot.start(token)


asyncio.run(main())
