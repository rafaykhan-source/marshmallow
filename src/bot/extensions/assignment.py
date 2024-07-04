"""This module represents a portion of the bot relevant to automatic role assignment.

The assignment module primarily operating on a Person ADT,
storing assignment result information.
"""

import asyncio
import logging

import dataproducer as dp
import discord
import settings as stg
import utility.datahandler as dh
import utility.processor as prep
from discord import Color, Embed
from discord.ext import commands, tasks
from settings import Server

logger = logging.getLogger("assign")


async def send_assignment_summary(
    ctx: commands.Context,
    found: int,
    not_found: int,
) -> None:
    """Sends assignment summary to context channel based on assignment stats.

    Args:
        ctx (commands.Context): The command context.
        found (int): The count of people found.
        not_found (int): The count of people not found.
    """
    embed = Embed(
        title="Role Assignment Summary",
        timestamp=discord.utils.utcnow(),
        color=Color.orange(),
    )

    embed.add_field(name="People Found:", value=str(found))
    embed.add_field(name="People Not Found:", value=str(not_found))
    if ctx.guild:
        embed.add_field(name="People on Server:", value=str(ctx.guild.member_count))

    await ctx.send(embed=embed)
    logger.info("Sent Role Assignment Summary.")

    return


async def is_valid_assignment(ctx: commands.Context, assignment_group: str) -> bool:
    """Returns validity of assign command call.

    Checks guild context and relevant constraints.

    Args:
        ctx (commands.Context): The command context.
        assignment_group (str): The assignment group.

    Returns:
        bool: A valid assign command call.
    """
    if not ctx.guild:
        return False

    match ctx.guild.id:
        case Server.FSI_ONLINE:
            options = {"online"}
            if assignment_group not in options:
                await ctx.send(
                    f"Invalid assignment group for this guild. Options: {options}.",
                )
                return False
        case Server.FSI_RESIDENTIAL:
            options = {"residential"}
            if assignment_group not in options:
                await ctx.send(
                    f"Invalid assignment group for this guild. Options: {options}.",
                )
                return False
        case Server.EBCAO_SUMMER:
            options = {"ebcscholars", "ebcstaff"}
            if assignment_group not in options:
                await ctx.send(
                    f"Invalid assignment group for this guild. Options: {options}.",
                )
                return False
        case Server.SIFP:
            options = {"sifpstudent", "sifpstaff", "mentorgroups"}
            if assignment_group not in options:
                await ctx.send(
                    f"Invalid assignment group for this guild. Options: {options}.",
                )
                return False
        case _:
            await ctx.send("Unsupported Guild.")
            return False

    return True


class Assignment(commands.Cog):
    """Cog for Role Assignment Commands.

    Holds the assign command.
    Holds the report_assignments command.

    Attributes:
        bot (commands.Bot): The bot.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the Assignment Cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        self.lock = asyncio.Lock()
        "The cog's lock."
        self.assign_cache: dict[str, commands.Context] = {}
        "The cog's cache for automatic role assignments."
        return

    @tasks.loop(minutes=15.0)
    async def assigner(self) -> None:
        """The protocol responsible for automatic role assignment.

        Args:
            ctx (commands.Context): The context object for automatic role assignment.
            assignment_group (str): The desired assignment group.
        """
        for assignment_group, ctx in self.assign_cache.items():
            async with self.lock:
                await self.assign(ctx, assignment_group)
        return

    def cache_assignment(self, ctx: commands.Context, assignment_group: str) -> None:
        """Caches the assignment task."""
        self.assign_cache[assignment_group] = ctx
        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def start_assigner(self, ctx: commands.Context, assignment_group: str) -> None:
        """Starts the automatic role assignment protocol."""
        self.assigner.start(ctx, assignment_group)
        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def stop_assigner(self, ctx: commands.Context) -> None:
        """Stops the automatic role assignment protocol."""
        self.assigner.cancel()
        await ctx.send("Stopped Assigner Protocol.")
        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def assign(
        self,
        ctx: commands.Context,
        assignment_group: str,
        role: discord.Role | None = None,
    ) -> None:
        """Automatically assigns roles for assignment group.

        Note that if override role is specified, then that will be assigned to
        assignment group.

        Args:
            ctx (commands.Context): The command context.
            assignment_group (str): The assignment group.
            role (discord.Role): An optional override role to assign.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'assign' for %s in %s.",
            ctx.author.display_name,
            assignment_group,
            ctx.guild.name,
        )

        if not await is_valid_assignment(ctx, assignment_group):
            return

        people = dp.get_people(assignment_group)
        member_alias_map = prep.create_member_alias_map(ctx.guild.members)

        for person in people:
            person.set_guild_member(member_alias_map)
            person.set_guild_roles(role)
        logger.info("Mapped People to Guild Members and Designated Guild Roles.")

        logger.info("Starting Role Assignments.")
        await ctx.send("*Starting Role Assignments.*")

        for person in people:
            await person.assign_roles(ctx)

        logger.info("Finished Role Assignments.")
        await ctx.send("*Finished Role Assignments.*")

        dh.write_assignment_report(people, assignment_group)
        await send_assignment_summary(ctx, *dh.get_assignment_counts(people))

        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def report_assignments(
        self,
        ctx: commands.Context,
        assignment_group: str,
    ) -> None:
        """Sends a report unidentified people.

        Args:
            ctx (commands.Context): The command context.
            assignment_group (str): The assignment group.
        """
        if not ctx.guild:
            return

        logger.info(
            "%s called command 'assign' for %s in %s.",
            ctx.author.display_name,
            assignment_group,
            ctx.guild.name,
        )
        await prep.send_failed_assignments(ctx, assignment_group)

        return


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Assignment(bot))
    return
