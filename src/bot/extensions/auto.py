"""This module represents a portion of the bot relevant to automatic role assignment.

This module maintains role-based role auto-assignments.
"""

import logging

import discord
import settings as stg
from discord.ext import commands
from settings import Server

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
        self.group_roles: list[discord.Role | None] = []
        "The group guild roles."
        self.group_to_nation: dict[str, str] = {
            "Zee Group 0": "Metal Clan",
            "Zee Group 1": "Metal Clan",
            "Zee Group 2": "Air Nomads",
            "Zee Group 3": "Air Nomads",
            "Zee Group 4": "Air Nomads",
            "Zee Group 5": "Earth Kingdom",
            "Zee Group 6": "Earth Kingdom",
            "Zee Group 7": "Earth Kingdom",
            "Zee Group 8": "Earth Kingdom",
            "Zee Group 9": "Fire Nation",
            "Zee Group 10": "Fire Nation",
            "Zee Group 11": "Fire Nation",
            "Zee Group 12": "Fire Nation",
            "Zee Group 13": "Water Tribe",
            "Zee Group 14": "Water Tribe",
            "Zee Group 15": "Water Tribe",
            "Zee Group 16": "Water Tribe",
        }
        "The mapping between group names and nation names for assignment."
        self.nation_to_role: dict[str, discord.Role | None] = {}
        "The mapping of nations to guild roles."
        return

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

        if not self.nation_to_role:
            self.nation_to_role = {
                nation: discord.utils.get(guild.roles, name=nation)
                for nation in self.nations
            }

        if not self.group_roles:
            self.group_roles = [
                discord.utils.get(guild.roles, name=group)
                for group in self.group_to_nation
            ]

        logger.info("Starting Nation Role Assignments.")
        await ctx.send("*Starting Nation Role Assignments.*")

        for group_role in self.group_roles:
            if not group_role:
                continue

            nation_name = self.group_to_nation[group_role.name]

            for member in group_role.members:
                nation_role = self.nation_to_role[nation_name]
                if not nation_role:
                    continue

                if nation_role in member.roles:
                    logger.info("%s already assigned %s.", member.name, nation_name)
                    continue

                await member.add_roles(nation_role)
                logger.info("%s was assigned %s.", member.name, nation_name)
                await ctx.send(f"{member.display_name} was assigned {nation_name}.")

        logger.info("Finished Nation Role Assignments.")
        await ctx.send("*Finished Nation Role Assignments.*")

        return


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Auto(bot))
    return
