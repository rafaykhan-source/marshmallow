"""This module represents the portion of the bot relevant to guild information.

Containing a cog, the information module stores several slash
commands used to get information about guild members.
"""

import logging

import discord
from discord import File
from discord.ext import commands

import marshmallow.settings as stg
import marshmallow.utility.dutils as du
from marshmallow.utility.datawriter import DataWriter


class Information(commands.Cog):
    """Cog for information-related commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the Information cog."""
        self.bot = bot
        "The cog's associated bot client."
        self.logger = logging.getLogger(__name__)
        "The cog's associated logger."
        self.writer: DataWriter = DataWriter()
        "A writer for data from the cog."

    @commands.hybrid_command()
    @commands.guild_only()
    async def about(self, ctx: commands.Context) -> None:
        """Sends Marshmallow's about message."""
        self.logger.info(
            "%s called command 'about' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        marshmallow_icon_file = File(
            "src/marshmallow/settings/resources/marshmallow_icon.png",
            filename="marshmallow_icon.png",
        )

        embed = du.get_basic_embed(
            title="About Marshmallow",
            description="Automates administrative and managerial tasks on Princeton EBCAO discords.",  # noqa: E501
        )

        embed.set_author(
            name="Marshmallow!",
            url="https://access.princeton.edu/",
            icon_url="attachment://marshmallow_icon.png",
        )
        embed.set_thumbnail(url="attachment://marshmallow_icon.png")
        embed.set_footer(
            text="Originally Developed by Rafay K '25",
            icon_url="attachment://marshmallow_icon.png",
        )

        await ctx.send(file=marshmallow_icon_file, embed=embed)
        self.logger.info("Sent About Message.")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def info(self, ctx: commands.Context, member: discord.Member) -> None:
        """Sends member information.

        Args:
            ctx (commands.Context): The command context.
            member (discord.Member): The member.
        """
        self.logger.info(
            "%s called command 'info' on %s in %s.",
            ctx.author.display_name,
            member.display_name,
            ctx.guild.name,
        )

        info_embed = du.get_basic_embed(title="Member Information")

        if member.joined_at:
            info_embed.add_field(
                name="Date Joined: ",
                value=discord.utils.format_dt(member.joined_at, style="F"),
                inline=False,
            )

        info_embed.add_field(name="Username: ", value=member.name)
        if hasattr(member, "global_name"):
            info_embed.add_field(name="Global Name: ", value=member.global_name)
        if member.nick:
            info_embed.add_field(name="Nick Name: ", value=member.nick)
        info_embed.add_field(
            name="Roles: ",
            value=", ".join([role.name for role in member.roles]),
            inline=False,
        )

        await ctx.send(embed=info_embed)
        self.logger.info("Sent Member Information.")

    # TODO: Add Embed Displaying Results
    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def get_message_count(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        start: du.DateTimeConverter,
        end: du.DateTimeConverter,
    ) -> None:
        """Writes message count from start to end date.

        Args:
            ctx (commands.Context): The command context.
            channel (discord.TextChannel): The channel to log activity for.
            start (str): Activity tracking start date, e.g. "02/15/23 12:53PM".
            end (str): Activity tracking end date "02/15/23 12:57PM".
        """
        self.logger.info(
            "%s called command 'get_message_count' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        messages = channel.history(limit=None, after=start, before=end)

        record = {}
        await ctx.send(f"Checking Message History of {channel.name}.")
        async for m in messages:
            person = (m.author.display_name, m.author.name)
            if person not in record:
                record[person] = 0
            record[person] += 1
        await ctx.send(f"Finished Checking Message History {channel.name}.")

        self.writer.write_message_counts(
            record,
            f"{channel.name[3:]}-{end.strftime('%m-%d-%y')}",
        )

        await ctx.send("Channel Activity Logged.")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def get_voice_channel_attendees(
        self,
        ctx: commands.Context,
        channel: discord.VoiceChannel,
    ) -> None:
        """Displays the current members in the specified voice channel.

        Args:
            ctx (commands.Context): The context object.
            channel (discord.VoiceChannel): The desired voice channel.
        """
        self.logger.info(
            "%s called command 'get_voice_channel_attendees' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        await ctx.send(embed=du.get_people_embed(channel.members))


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Information(bot))
