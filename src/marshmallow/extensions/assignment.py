"""This module represents a portion of the bot relevant to automatic role assignment.

The assignment module primarily operating on a Person models,
storing assignment result information.
"""

import asyncio
import logging

import discord
from discord.ext import commands, tasks

import marshmallow.settings as stg
import marshmallow.utility.dutils as du
import marshmallow.utility.processor as pr
from marshmallow.settings import Server
from marshmallow.utility.dataproducer import DataServer
from marshmallow.utility.datawriter import DataWriter


async def is_valid_assignment(ctx: commands.Context, assignment_group: str) -> bool:  # noqa
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
            options = {"sifp", "mentorgroups"}
            if assignment_group not in options:
                await ctx.send(
                    f"Invalid assignment group for this guild. Options: {options}.",
                )
                return False
        case Server.FGLI_CONSORTIUM:
            options = {"fgli"}
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
    """A cog for role assignment commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the Assignment cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        self.logger = logging.getLogger(__name__)
        "The cog's associated logger."
        self.lock = asyncio.Lock()
        "The cog's lock."
        self.assign_cache: dict[str, commands.Context] = {}
        "The cog's cache for automatic role assignments."
        self.server: DataServer = DataServer()
        "A server for data needed in the cog."
        self.writer: DataWriter = DataWriter()
        "A writer for data from the cog."

    @tasks.loop(minutes=15.0)
    async def assigner(self) -> None:
        """The protocol responsible for automatic role assignment.

        Args:
            ctx (commands.Context): The context object for automatic role assignment.
            assignment_group (str): The desired assignment group.
        """
        for group, ctx in self.assign_cache.items():
            async with self.lock:
                await self.assign(ctx, group)

    def cache_assignment(self, ctx: commands.Context, assignment_group: str) -> None:
        """Caches the assignment task."""
        self.assign_cache[assignment_group] = ctx

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def start_assigner(self, ctx: commands.Context) -> None:
        """Starts the automatic role assignment protocol."""
        await ctx.send("Started Assigner Protocol.")
        self.assigner.start()

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def stop_assigner(self, ctx: commands.Context) -> None:
        """Stops the automatic role assignment protocol."""
        self.assigner.cancel()
        await ctx.send("Stopped Assigner Protocol.")

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

        self.logger.info(
            "%s called command 'assign' for %s in %s.",
            ctx.author.display_name,
            assignment_group,
            ctx.guild.name,
        )

        if not await is_valid_assignment(ctx, assignment_group):
            return

        self.cache_assignment(ctx, assignment_group)
        people = self.server.get_people(assignment_group)
        member_alias_map = pr.get_member_guild_name_map(ctx.guild.members)

        for person in people:
            person.set_guild_member(member_alias_map)
            person.set_guild_roles(role)
        self.logger.info("Mapped People to Guild Members and Designated Guild Roles.")

        self.logger.info("Starting Role Assignments.")
        await ctx.send("*Starting Role Assignments.*")

        for person in people:
            await person.assign_roles(ctx)

        self.logger.info("Finished Role Assignments.")
        await ctx.send("*Finished Role Assignments.*")

        self.writer.write_assignment_report(people, assignment_group)
        embed = du.get_assignment_summary_embed(ctx, *pr.get_assignment_counts(people))
        await ctx.send(embed=embed)

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

        self.logger.info(
            "%s called command 'assign' for %s in %s.",
            ctx.author.display_name,
            assignment_group,
            ctx.guild.name,
        )

        people = self.server.get_report_people(assignment_group)
        await ctx.send(embed=du.get_failed_assignments_embed(people, assignment_group))


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Assignment(bot))
