"""This module represents a portion of the bot relevant to automatic role assignment.

This module maintains role-based role auto-assignments.
"""

import logging

from discord.ext import commands

import marshmallow.settings as stg
import marshmallow.utility.dmaps as dm
import marshmallow.utility.processor as pr
from marshmallow.utility.dataproducer import DataServer
from marshmallow.utility.datawriter import DataWriter


class Affinity(commands.Cog):
    """A cog for affinity commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        self.logger = logging.getLogger(__name__)
        "The cog's associated logger."
        self.server: DataServer = DataServer()
        "A server for data for the cog."
        self.writer: DataWriter = DataWriter()
        "A writer for data from the cog."

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def assign_affinity(self, ctx: commands.Context, group: str) -> None:
        """Assigns affinity groups.

        Args:
            ctx (commands.Context): The command context.
            group (str): The group to assign roles.
        """
        self.logger.info(
            "%s called command 'assign_affinity' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        channel_names = [
            "💬│fli-rural",
            "💬│fli-muslim",
            "💬│fli-apida",
            "💬│fli-black",
            "💬│fli-christian",
            "💬│fli-latine",
            "💬│fli-mena",
            "💬│fli-women-femmes-of-color",
            "💬│fli-ability",
            "💬│fli-transfer-and-vets",
            "💬│q-q-f-f",
            "💬│fli-indigenous",
            "💬│fli-international",
            "💬│fli-foster",
            # "fli-rural-lead",
            # "fli-muslim-lead",
            # "fli-mena-lead",
            # "fli-apida-lead",
            # "fli-black-lead",
            # "fli-christian-lead",
            # "fli-latine-lead",
            # "fli-women-femmes-of-color-lead",
            # "fli-ability-lead",
            # "fli-transfer-and-vets-lead",
            # "q-q-f-f-lead",
            # "fli-indigenous-lead",
            # "fli-international-lead",
            # "fli-foster-lead",
        ]

        people = self.server.get_people(group)
        member_alias_map = pr.get_member_guild_name_map(ctx.guild.members)
        channel_map = await dm.get_channel_map(ctx, channel_names)
        management = self.bot.get_cog("Management")

        for p in people:
            if not p.info.affinity_groups:
                self.logger.info(
                    "%s has no affinity groups: %s",
                    p.info.full_name,
                    p.info.affinity_groups,
                )
                continue

            p.set_guild_member(member_alias_map)
            if not p.guild_member:
                continue

            # TODO: Remove line below and come up with better solution for naming.
            affinity_groups = [
                ch for ch in channel_names for a in p.info.affinity_groups if a in ch
            ]
            channels = [channel_map[g] for g in affinity_groups if g in channel_map]

            for ch in channels:
                await management.grant_channel_access(ctx, p.guild_member, ch)

        self.writer.write_assignment_report(people, group)
        await ctx.send("Affinity Assignments Completed.")


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Affinity(bot))
