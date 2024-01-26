"""A module containing settings information pertinent to bot usage.

This module contains functions that standardize the customizable
properties of discord.py's commands.Bot and amenable to usage on
EBCAO Guilds.
"""

import logging
import os
import random
import sys
from enum import IntEnum, unique

import discord
import yaml
from dotenv import load_dotenv

logger = logging.getLogger("marshmallow")


def get_token() -> str:
    """Returns bot token.

    Returns:
        str: The bot token.

    Raises:
        ValueError: Token not found.
    """
    load_dotenv()

    try:
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            msg = "Token Not Found."
            raise ValueError(msg)

    except ValueError as ex:
        logger.error(ex)
        sys.exit(1)

    return token


def get_cog_names() -> set[str]:
    """Returns cog names.

    Returns:
        set[str]: The cog names.
    """
    cogs = set()
    for file in os.listdir("src/bot/extensions/"):
        if file.endswith(".py"):
            cogs.add(file[:-3])

    return cogs


# TODO: Convert to bot_check
def get_admin_roles() -> list[str]:
    """Returns admin role names.

    Returns:
        list[str]: The admin role names.
    """
    return [
        "EBCAO Discord Admin",
        "SIFP Discord Admin",
        "Tech CA",
        "Admin",
    ]


def get_logging_config() -> dict:
    """Returns bot's logging configuration as a dictionary.

    Returns:
        dict: The logger configuration.
    """
    with open(
        "src/bot/settings/logging_config.yml",
        encoding="UTF-8",
    ) as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as ex:
            logger.error("YAML Error: %s", ex)

    return config


def get_command_prefix() -> str:
    """Returns Marshmallow's command prefix.

    Returns:
        str: Marshmallow's command prefix.
    """
    return "!"


def get_random_discord_activity() -> discord.BaseActivity:
    """Returns a random discord activity.

    Returns:
        discord.BaseActivity: A random discord activity.
    """
    load_dotenv()
    options = [
        discord.Game(os.getenv("GAME1", "Game Not Found.")),
        discord.Game(os.getenv("GAME2", "Game Not Found.")),
        discord.Activity(
            type=discord.ActivityType.watching,
            name="Avatar the Last Airbender",
        ),
    ]
    return random.choice(options)


def get_intents() -> discord.Intents:
    """Returns intents for Marshmallow Bot.

    Fully disabled intent object is constructed, and
    intent attributes are manually enabled with comment
    above for justification.

    Returns:
        discord.Intents: The bot intents.
    """
    intents = discord.Intents.none()
    # Guild and all its attributes.
    intents.guilds = True
    # Handles on_member_join()
    intents.members = True
    # Utilizes Message Objects
    intents.guild_messages = True
    # Looking at Message Content for Command Call
    intents.message_content = True

    return intents


# TODO: Create another bot check from this
@unique
class Server(IntEnum):
    """A Server Class to Store Relevant Guild IDs."""

    load_dotenv()
    SIFP = os.getenv("SIFP")
    FSI_ONLINE = os.getenv("FSI_ONLINE")
    FSI_RESIDENTIAL = os.getenv("FSI_RESIDENTIAL")
    EBCAO_SUMMER = os.getenv("EBCAO_SUMMER")
    MARSHMALLOW_DEV = os.getenv("MARSHMALLOW_DEV")


def main() -> None:
    """Unit Testing."""
    return


if __name__ == "__main__":
    main()
