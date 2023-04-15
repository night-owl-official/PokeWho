import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
token = os.getenv("TOKEN")
cmd_prefix = os.getenv("COMMAND_PREFIX")

description = """Guess the Pokemon!
The bot will show an image representing a random Pokemon,
and the user will have to guess who that Pokemon is by entering its name."""

intents = discord.Intents.default()
intents.message_content = True

poke_who = commands.Bot(command_prefix=cmd_prefix,
                        description=description, intents=intents)


@poke_who.event
async def on_ready():
    print(f"Logged in as {poke_who.user} (ID: {poke_who.user.id})")
    print("-------")

poke_who.run(token)