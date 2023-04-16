import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context
import asyncio
from typing import Literal, Optional

from pokemon_cog import PokemonCog

load_dotenv()
token = os.getenv("TOKEN")

description = """
**Guess the Pokemon!**
The bot will show an image representing a random Pokemon, 
and the user will have to guess who that Pokemon is by entering its name.
"""

intents = discord.Intents.default()
intents.message_content = True

poke_who = commands.Bot(command_prefix='?',
                        description=description, intents=intents)

poke_who.remove_command("help")


@poke_who.event
async def on_ready():
    print(f"Logged in as {poke_who.user} (ID: {poke_who.user.id})")
    print("-------")


@poke_who.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            # Sync commands to the current guild
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            # Copy all global commands to the current guild and syncs
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            # Clear all commands from the current guild and syncs
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            # Sync commands globally
            synced = await ctx.bot.tree.sync()

        await ctx.send(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}")
        return

    # Sync commands to all given guilds and keep track of
    # the successful attempts
    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def main():
    async with poke_who:
        await poke_who.add_cog(PokemonCog(poke_who))
        await poke_who.start(token)

asyncio.run(main())
