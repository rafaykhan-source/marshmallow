"""This module represents the portion of the bot relevant to live bot development.

This allows for code to be modified and reloaded without having to take the bot offline.

Containing a cog, the development module stores several slash
commands relevant to live bot development.
"""

import logging

from discord.ext import commands

import marshmallow.settings as stg
from marshmallow.settings import Server


class Development(commands.Cog):
    """Cog for development commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Instantiates the development cog."""
        self.bot: commands.Bot = bot
        "The cog's associated bot client."
        self.logger = logging.getLogger(__name__)
        "The cog's associated logger."
        self.cog_names: set[str] = stg.get_cog_names()
        "The cogs of the bot."

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def sync(self, ctx: commands.Context) -> None:
        """Syncs guild slash commands.

        Args:
            ctx (commands.Context): The command context.
        """
        if not ctx.guild:
            return

        self.logger.info(
            "%s called command 'sync' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )
        if ctx.guild.id != Server.MARSHMALLOW_DEV:
            self.logger.warning("'sync' command was called in incorrect guild.")
            await ctx.send("Wrong Server.")
            return

        await self.bot.tree.sync()
        self.logger.info("Synced Slash Commands.")
        await ctx.send("Synced Guild Slash Commands.")

        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def reload(self, ctx: commands.Context, cog_name: str) -> None:
        """Reloads specified cog.

        Args:
            ctx (commands.Context): The command context.
            cog_name (str): The cog to reload.
        """
        if not ctx.guild or cog_name not in self.cog_names:
            await ctx.send(f"{cog_name} is not in cogs.")
            return
        self.logger.info(
            "%s called command 'reload' for %s in %s.",
            ctx.author.display_name,
            cog_name,
            ctx.guild.name,
        )

        await self.bot.reload_extension(f"extensions.{cog_name}")
        self.logger.info("Reloaded Cog: %s", cog_name)
        await ctx.send(f'"*{cog_name}*" Cog Reloaded.')

        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def load(self, ctx: commands.Context, cog_name: str) -> None:
        """Loads specified cog.

        Args:
            ctx (commands.Context): The command context.
            cog_name (str): The cog to load.
        """
        if not ctx.guild or cog_name not in self.cog_names:
            await ctx.send(f"{cog_name} is not in cogs.")
            return
        self.logger.info(
            "%s called command 'load' for %s in %s.",
            ctx.author.display_name,
            cog_name,
            ctx.guild.name,
        )

        await self.bot.load_extension(f"extensions.{cog_name}")
        self.logger.info("Loaded Cog: %s", cog_name)
        await ctx.send(f'"*{cog_name}*" Cog Loaded.')

        return

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def unload(self, ctx: commands.Context, cog_name: str) -> None:
        """Unloads specified cog.

        Args:
            ctx (commands.Context): The command context.
            cog_name (str): The cog to unload.
        """
        if not ctx.guild or cog_name not in self.cog_names:
            await ctx.send(f"{cog_name} is not in cogs.")
            return
        self.logger.info(
            "%s called command 'unload' for %s in %s.",
            ctx.author.display_name,
            cog_name,
            ctx.guild.name,
        )

        await self.bot.unload_extension(f"extensions.{cog_name}")
        self.logger.info("Unloaded Cog: %s", cog_name)
        await ctx.send(f'"*{cog_name}*" Cog Unloaded.')

        return

    @commands.hybrid_command(name="reloadall")
    @commands.guild_only()
    @commands.has_any_role(*stg.get_admin_roles())
    async def reload_all(self, ctx: commands.Context) -> None:
        """Reloads all cogs.

        Args:
            ctx (commands.Context): The command context.
        """
        if not ctx.guild:
            return
        self.logger.info(
            "%s called command 'reloadall' in %s.",
            ctx.author.display_name,
            ctx.guild.name,
        )

        for name in self.cog_names:
            await self.reload(ctx, name)
        self.logger.info("Reloaded all Cogs.")
        await ctx.send("Reloaded all Cogs.")

        return


async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot."""
    await bot.add_cog(Development(bot))
