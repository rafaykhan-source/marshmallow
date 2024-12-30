"""This package represents Marshmallow's custom settings/configuration."""

from marshmallow.settings.config import (
    Server,
    configure_logging,
    get_admin_roles,
    get_cog_names,
    get_command_prefix,
    get_intents,
    get_random_discord_activity,
    get_token,
)

__all__ = [
    "Server",
    "configure_logging",
    "get_admin_roles",
    "get_cog_names",
    "get_command_prefix",
    "get_intents",
    "get_random_discord_activity",
    "get_token",
]
