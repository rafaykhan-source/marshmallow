"""This module is responsible for running Marshmallow."""

import logging
import logging.config

import settings as stg
from marshmallow import MarshmallowBotClient

logger = logging.getLogger("run")


def __configure_logging() -> None:
    """Configures logging."""
    config = stg.get_logging_config()
    logging.config.dictConfig(config)

    return


def main() -> None:
    """Runs Marshmallow."""
    __configure_logging()

    logger.info("Instantiating Marshmallow Bot Client.")
    bot = MarshmallowBotClient()

    logger.info("Retrieving Token.")
    TOKEN = stg.get_token()  # noqa

    logger.info("Starting Marshmallow.")
    bot.run(TOKEN, log_handler=None)

    return


if __name__ == "__main__":
    main()
