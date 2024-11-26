"""Initializes the marshmallow package."""

import logging

import marshmallow.settings as stg


def __configure_logging() -> None:
    """Configures logging."""
    config = stg.get_logging_config()
    logging.config.dictConfig(config)


__configure_logging()
