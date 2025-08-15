import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))

intents = discord.Intents.all()
activity = discord.Game(name="MelonVillage SMP")

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extensions()

        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    async def load_extensions(self):
        for filename in os.listdir('./commands'):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await self.load_extension(f'commands.{filename[:-3]}')
                except Exception as e:
                    pass

bot = MyBot(
    command_prefix="!",
    intents=intents,
    activity=activity,
    status=discord.Status.online
)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Erreur: {error}", ephemeral=True)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
