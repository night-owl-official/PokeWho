import discord
from discord.ext import commands
import asyncio
import requests
import random

pokeapi_url = "https://pokeapi.co/api/v2/pokemon/"
pokemon_gif_url = "https://play.pokemonshowdown.com/sprites/ani/"


class PokemonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timeout = 10.0

    @commands.command(name="pokemon", aliases=["p"], help="Generate a random pokemon")
    async def get_random_pokemon(self, ctx: commands.Context):
        try:
            rand_poke_id = random.randint(1, 905)
            api_request = requests.get(f"{pokeapi_url}{rand_poke_id}")
            response_json = api_request.json()

            pokemon_name = response_json["name"]

            pokemon_embed = discord.Embed(
                title="Who's this Pokemon?!", color=discord.Color.random())
            pokemon_embed.set_image(url=f"{pokemon_gif_url}{pokemon_name}.gif")
            await ctx.send(embed=pokemon_embed)

            def is_correct(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            try:
                guess = await self.bot.wait_for("message", check=is_correct, timeout=self.timeout)
            except asyncio.TimeoutError:
                return await ctx.send(f"Sorry, you took too long. The answer was {pokemon_name}")

            if guess.content.lower() == pokemon_name.lower():
                await ctx.send("Correct!!")
            else:
                await ctx.send(f"Oops. It's actually {pokemon_name}.")
        except:
            await ctx.send("Error retrieving data from the API")
