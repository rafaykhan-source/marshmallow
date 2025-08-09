"""This module represents a portion of the bot relevant to automatic role assignment."""

import asyncio
import logging
from enum import StrEnum, auto

from discord.ext import commands, tasks

import marshmallow.settings as stg
import marshmallow.utility.dutils as du
import marshmallow.utility.processor as pr
from marshmallow.utility.dataproducer import DataServer
from marshmallow.utility.datawriter import DataWriter
from marshmallow.utility.dutils import log_send


class Group(StrEnum):
    """The assignment groups."""

    RESIDENTIAL = auto()
    ONLINE = auto()
    SIFP = auto()


class Assignment(commands.Cog):
    """A cog for assignment commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the cog."""
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
        await log_send(ctx, self.logger, "Started Assigner Protocol.")
        self.assigner.start()

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def stop_assigner(self, ctx: commands.Context) -> None:
        """Stops the automatic role assignment protocol."""
        self.assigner.cancel()
        await log_send(ctx, self.logger, "Stopped Assigner Protocol.")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    @commands.has_permissions(manage_roles=True)
    async def assign(
        self,
        ctx: commands.Context,
        group: Group,
    ) -> None:
        """Automatically assigns roles for assignment group.

        Note that if override role is specified, then that will be assigned to
        assignment group.

        Args:
            ctx (commands.Context): The command context.
            group (str): The assignment group.
        """
        self.logger.info(
            "%s called command 'assign' for %s in %s.",
            ctx.author.display_name,
            group,
            ctx.guild.name,
        )

        self.cache_assignment(ctx, group)
        people = self.server.get_people(group)
        member_alias_map = pr.get_member_guild_name_map(ctx.guild.members)

        for p in people:
            p.set_guild_member(member_alias_map)
            p.set_guild_roles()
        self.logger.info("Mapped People to Guild Members and Designated Guild Roles.")

        await log_send(ctx, self.logger, "*Starting Role Assignments.*")
        for p in people:
            await p.assign_roles(ctx)
        await log_send(ctx, self.logger, "*Finished Role Assignments.*")

        self.writer.write_assignment_report(people, group)
        found, not_found = pr.get_assignment_counts(people)
        embed = du.get_assignment_summary_embed(ctx, found, not_found)
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
