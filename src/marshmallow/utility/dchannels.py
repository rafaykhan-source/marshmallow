"""The dchannels module contains utility functions for discord channels."""

import discord


def get_basic_access_overwrite(
    channel: discord.TextChannel | discord.VoiceChannel,
) -> discord.PermissionOverwrite:
    """Returns a basic access overwrite based on channel.

    Args:
        channel (discord.TextChannel | discord.VoiceChannel): The channel to overwrite.

    Returns:
        PermissionOverwrite: The overwrite.
    """
    overwrite = discord.PermissionOverwrite()
    if isinstance(channel, discord.TextChannel):
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.read_message_history = True
    if isinstance(channel, discord.VoiceChannel):
        overwrite.connect = True
        overwrite.use_soundboard = True
        overwrite.use_voice_activation = True
        overwrite.speak = True
        overwrite.view_channel = True
        overwrite.stream = True

    return overwrite


if __name__ == "__main__":
    pass
