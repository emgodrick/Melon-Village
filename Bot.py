import discord
from discord.ext import commands
from discord import app_commands
import os
from config import DISCORD_TOKEN

GUILD_ID = 1293979587264380928

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

activity = discord.Game(name="MelonVillage SMP")

class MyBot(commands.Bot):
    async def setup_hook(self):
        for file in os.listdir("./commands"):
            if file.endswith(".py") and file != "__init__.py":
                await self.load_extension(f"commands.{file[:-3]}")
        # Synchronisation forcée des commandes
        await self.tree.sync()
        print("Commandes synchronisées avec succès!")

bot = MyBot(
    command_prefix="!",
    intents=intents,
    activity=activity,
    status=discord.Status.online
)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    print("Liste des commandes disponibles:")
    for command in bot.tree.get_commands():
        print(f"- /{command.name}")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Erreur: {error}", ephemeral=True)

bot.run(DISCORD_TOKEN)
