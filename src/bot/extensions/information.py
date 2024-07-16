"""This module represents the portion of the bot relevant to guild information.

Containing a cog, the information module stores several slash
commands used to get information about guild members.
"""

import logging

import discord
import settings as stg
import utility.datahandler as dh
import utility.dutils as du
from discord import File
from discord.ext import commands

logger = logging.getLogger("commands")


class Information(commands.Cog):
    """Cog for information-related commands.

    Holds the about command.
    Holds the info command.
    Holds the get_channel_activity command.

    Attributes:
        bot (commands.Bot): The bot.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the Information Cog."""
        self.bot = bot
        return

    @commands.hybrid_command()
    @commands.guild_only()
    async def about(self, ctx: commands.Context) -> None:
        """Sends Marshmallow's about message."""
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'about' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        marshmallow_icon_file = File(
            "src/bot/settings/resources/marshmallow_icon.png",
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
        logger.info("Sent About Message.")

        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def info(self, ctx: commands.Context, member: discord.Member) -> None:
        """Sends member information.

        Args:
            ctx (commands.Context): The command context.
            member (discord.Member): The member.
        """
        if not ctx.guild:
            return

        logger.info(
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
        logger.info("Sent Member Information.")

        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def get_channel_activity(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        *,
        start: du.DateTimeConverter,
    ) -> None:
        """Maps people's daily message activity in channel from start date.

        Args:
            ctx (commands.Context): The command context.
            channel (discord.TextChannel): Channel to log activity for.
            start (str): Activity tracking start date "mm/dd/yyyy".
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'get_channel_activity' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        messages = channel.history(limit=None, after=start)

        record: dict[str, set[str]] = {}
        await ctx.send(f"Checking Message History of {channel.name}.")
        async for msg in messages:
            person = f"{msg.author.display_name} ({msg.author.name})"
            msg_date = msg.created_at.strftime("%m/%d/%Y")
            if person not in record:
                record[person] = set()
            record[person].add(msg_date)
        await ctx.send(f"Finished Checking Message History {channel.name}.")

        sorted_record = {person: sorted(dates) for person, dates in record.items()}
        dh.write_daily_message_report(sorted_record, channel.name)

        await ctx.send("Channel Activity Logged.")


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Information(bot))
    return
