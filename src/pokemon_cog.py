import discord
from discord import app_commands
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
        self.pokemon_name = None

    async def set_random_pokemon(self):
        rand_poke_id = random.randint(1, 905)

        try:
            # Get request to pokeapi for a random pokemon id
            # Extract json from the response and access the name field
            api_request = requests.get(f"{pokeapi_url}{rand_poke_id}")
            response_json = api_request.json()

            self.pokemon_name = response_json["name"]
        except requests.exceptions.RequestException as e:
            print(e)

    def get_pokemon_embed(self) -> discord.Embed:
        pokemon_embed = discord.Embed(
            title="Who's this Pokemon?!", color=discord.Color.random())

        pokemon_embed.set_image(
            url=f"{pokemon_gif_url}{self.pokemon_name}.gif")

        return pokemon_embed

    def is_guess_correct(self, guess: str) -> bool:
        return guess.content.lower() == self.pokemon_name.lower()

    @app_commands.command(name="pokemon", description="Generate a random Pokemon and wait for a guess")
    async def pokemon(self, interaction: discord.Interaction):
        await self.set_random_pokemon()

        # Make sure the bot doesn't continue running if there was some issues with the api request
        if (self.pokemon_name != None):
            await interaction.response.send_message(embed=self.get_pokemon_embed())

            # Check if whoever fired the command in a channel
            # is the same user that responded to the bot in that same channel
            def is_correct(msg):
                return msg.author == interaction.user and msg.channel == interaction.channel

            # User has a time limit to take a guess, after which the bot will stop waiting
            try:
                guess = await self.bot.wait_for("message", check=is_correct, timeout=self.timeout)
            except asyncio.TimeoutError:
                return await interaction.followup.send(f"**Sorry, you took too long. The answer was** *{self.pokemon_name}*", ephemeral=True)

            if self.is_guess_correct(guess):
                await interaction.followup.send(":tada: **Correct!!** :tada:", ephemeral=True)
            else:
                await interaction.followup.send(f"**Oops** :tired_face: **It's actually** *{self.pokemon_name}.*", ephemeral=True)
        else:
            await interaction.response.send_message("**I'm having issues...** :cry:")
