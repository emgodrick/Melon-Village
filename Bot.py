import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

activity = discord.Game(name="MelonVillage SMP")

class MyBot(commands.Bot):
    async def setup_hook(self):
        print("\n" + "="*50)
        print("🚀 Initialisation du bot...")
        print("="*50 + "\n")
        
        await self.load_extensions()

        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print("\n" + "="*50)
        print("✅ Synchronisation des commandes Discord terminée")
        print("="*50)

    async def load_extensions(self):
        print("\n📚 Chargement des extensions :")
        print("-"*30)
        for filename in os.listdir('./commands'):
            if filename.endswith('.py') and filename != '__init__.py':
                await self.load_extension(f'commands.{filename[:-3]}')
                print(f"  ✓ {filename[:-3]}")
        print("-"*30)

bot = MyBot(
    command_prefix="!",
    intents=intents,
    activity=activity,
    status=discord.Status.online
)

@bot.event
async def on_ready():
    print("\n" + "="*50)
    print(f"🤖 Bot connecté avec succès")
    print(f"📝 Nom : {bot.user.name}")
    print(f"🆔 ID : {bot.user.id}")
    print("="*50)
    
    print("\n✨ Bot prêt à être utilisé !")
    print("="*50 + "\n")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Erreur: {error}", ephemeral=True)

bot.run(DISCORD_TOKEN)
