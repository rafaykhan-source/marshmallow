"""This module represents a portion of the bot relevant to automatic role assignment.

This module maintains role-based role auto-assignments.
"""

import logging
from typing import TYPE_CHECKING

import settings as stg
import utility.dataproducer as dp
import utility.dmaps as dm
import utility.processor as pr
from discord.ext import commands
from settings import Server

if TYPE_CHECKING:
    import discord

logger = logging.getLogger("assign")


class Auto(commands.Cog):
    """Cog for Auto Assignment Specific Commands.

    Holds the assign_nations command.

    Attributes:
        bot (commands.Bot): The bot.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the Auto Cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        self.nations: set[str] = {
            "Metal Clan",
            "Air Nomads",
            "Earth Kingdom",
            "Fire Nation",
            "Water Tribe",
        }
        "The nation names for assignment."
        self.group_map: dict[str, discord.Role | None] = {}
        "The mapping of groups to guild roles."
        self.group_to_nation: dict[str, str] = {
            "Zee Group 0": "Metal Clan",
            "Zee Group 1": "Metal Clan",
            "Zee Group 2": "Air Nomads",
            "Zee Group 3": "Air Nomads",
            "Zee Group 4": "Earth Kingdom",
            "Zee Group 5": "Earth Kingdom",
            "Zee Group 6": "Earth Kingdom",
            "Zee Group 7": "Fire Nation",
            "Zee Group 8": "Fire Nation",
            "Zee Group 9": "Fire Nation",
            "Zee Group 10": "Fire Nation",
            "Zee Group 11": "Fire Nation",
            "Zee Group 12": "Water Tribe",
            "Zee Group 13": "Water Tribe",
            "Zee Group 14": "Water Tribe",
            "Zee Group 15": "Water Tribe",
            "Zee Group 16": "Water Tribe",
            "Zee Group 17": "Water Tribe",
        }
        "The mapping between group names and nation names for assignment."
        self.nation_map: dict[str, discord.Role | None] = {}
        "The mapping of nations to guild roles."

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def assign_nations(self, ctx: commands.Context) -> None:
        """Assigns guild members their avatar nations based on zee group.

        Args:
            ctx (commands.Context): The command context.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'assign_nations' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )
        guild = ctx.guild

        if guild.id not in [Server.FSI_ONLINE, Server.MARSHMALLOW_DEV]:
            logger.debug(
                "'/assign_nations' command was called in incorrect guild: %s",
                guild.name,
            )
            await ctx.send("Wrong Guild.")
            return

        if not self.nation_map:
            self.nation_map = await dm.get_role_map(ctx, list(self.nations))

        if not self.group_map:
            self.group_map = await dm.get_role_map(
                ctx,
                list(self.group_to_nation.keys()),
            )

        logger.info("Starting Nation Role Assignments.")
        await ctx.send("*Starting Nation Role Assignments.*")

        for group_name, group_role in self.group_map.items():
            if not group_role:
                continue

            nation_name = self.group_to_nation[group_name]
            nation_role = self.nation_map[nation_name]
            if not nation_role:
                continue

            for m in group_role.members:
                if nation_role in m.roles:
                    logger.info("%s already assigned %s.", m.name, nation_name)
                    continue

                await m.add_roles(nation_role)
                logger.info("%s was assigned %s.", m.name, nation_name)
                await ctx.send(f"{m.display_name} was assigned {nation_name}.")

        logger.info("Finished Nation Role Assignments.")
        await ctx.send("*Finished Nation Role Assignments.*")

        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def assign_affinity(self, ctx: commands.Context) -> None:
        """Assigns affinity groups.

        Args:
            ctx (commands.Context): The command context.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'assign_affinity' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        people = dp.get_affinity_people()
        channel_names = [
            "💬│fli-rural",
            "💬│fli-muslim",
            "💬│fli-apida",
            "💬│fli-black",
            "💬│fli-christian",
            "💬│fli-latine",
            "💬│fli-women-femmes-of-color",
            "💬│fli-ability",
            "💬│fli-transfer-and-vets",
            "💬│q-q-f-f",
            "💬│fli-indigenous",
            "💬│fli-international",
            "💬│fli-foster",
            "fli-rural-lead",
            "fli-muslim-lead",
            "fli-apida-lead",
            "fli-black-lead",
            "fli-christian-lead",
            "fli-latine-lead",
            "fli-women-femmes-of-color-lead",
            "fli-ability-lead",
            "fli-transfer-and-vets-lead",
            "q-q-f-f-lead",
            "fli-indigenous-lead",
            "fli-international-lead",
            "fli-foster-lead",
        ]

        text_channels = await dm.get_channel_map(ctx, channel_names)
        member_alias_map = pr.create_member_alias_map(ctx.guild.members)

        for person in people:
            member = None
            alg_names = person["alg_names"]
            for mem, aliases in member_alias_map.items():
                if pr.is_name_match(aliases, alg_names):
                    member = mem
                    break

            groups = person["affinity_groups"]
            channels = [text_channels[g] for g in groups if g in text_channels]

            management = self.bot.get_cog("Management")
            for ch in channels:
                await management.grant_channel_access(ctx, member, ch)


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Auto(bot))
