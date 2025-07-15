"""This module is responsible for running Marshmallow."""

import asyncio
import logging

from marshmallow.bot import MarshmallowBot
from marshmallow.settings import get_token


async def main() -> None:
    """Runs Marshmallow."""
    logger = logging.getLogger("run")

    logger.info("Instantiating Marshmallow Bot Client.")
    marshmallow = MarshmallowBot()

    logger.info("Retrieving Token.")
    token = get_token()

    async with marshmallow as bot:
        logger.info("Starting Marshmallow.")
        await bot.start(token)


asyncio.run(main())
