from discord.ext import commands
import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context  # or a subclass of yours
from typing import Literal, Optional


class Sync(commands.Cog):
    """The description for Sync goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def cogs(self, ctx: Context, action: str, cog_name: str):
        if action == "load":
            await self.bot.load_extension(f"cogs.{cog_name}")

        if action == "reload":
            if self.bot.get_cog(cog_name.title()) is not None:
                await self.bot.unload_extension(f"cogs.{cog_name}")
                await self.bot.load_extension(f"cogs.{cog_name}")
                await ctx.reply(":3")
            else:
                await ctx.reply("cog not loaded dumbass")


async def setup(bot):
    await bot.add_cog(Sync(bot))
