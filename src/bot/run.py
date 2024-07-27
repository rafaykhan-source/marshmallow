"""This module is responsible for running Marshmallow."""

import asyncio
import logging
import logging.config

import settings as stg
from marshmallow import MarshmallowBotClient

logger = logging.getLogger("run")


def __configure_logging() -> None:
    """Configures logging."""
    config = stg.get_logging_config()
    logging.config.dictConfig(config)


async def main() -> None:
    """Runs Marshmallow."""
    __configure_logging()

    logger.info("Instantiating Marshmallow Bot Client.")
    marsh = MarshmallowBotClient()

    logger.info("Retrieving Token.")

    async with marsh as bot:
        logger.info("Starting Marshmallow.")
        await bot.start(stg.get_token())


if __name__ == "__main__":
    asyncio.run(main())
