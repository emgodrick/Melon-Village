import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys

load_dotenv()

GUILD_ID = int(os.getenv('GUILD_ID', 0))
OWNER_ID = int(os.getenv('OWNER_ID', 0))

class Shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shutdown", description="Éteint le bot (Admin uniquement)")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def shutdown(self, interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("Seulement Emgodrick peut utiliser cette commande.", ephemeral=True)
            return

        await self.bot.close()
        sys.exit(0)

async def setup(bot):
    await bot.add_cog(Shutdown(bot)) 