import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv('GUILD_ID', 0))
OWNER_ID = int(os.getenv('OWNER_ID', 0))

AUTO_MOD_ENABLED = True

class ModerationControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ensure_auto_mod_enabled()

    def ensure_auto_mod_enabled(self):
        global AUTO_MOD_ENABLED
        AUTO_MOD_ENABLED = True

    @app_commands.command(name="automod", description="Active ou désactive la modération automatique")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.describe(state="on ou off")
    async def automod(self, interaction: discord.Interaction, state: str):
        global AUTO_MOD_ENABLED

        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("Seulement le owner du serveur peut exécuter cette commande", ephemeral=True)
            return

        if state.lower() == "on":
            AUTO_MOD_ENABLED = True
            await interaction.response.send_message("Modération automatique activée.")
        elif state.lower() == "off":
            AUTO_MOD_ENABLED = False
            await interaction.response.send_message("Modération automatique désactivée.")
        else:
            await interaction.response.send_message("Valeur invalide. Utilise 'on' ou 'off'.")

    def is_auto_mod_enabled(self):
        return AUTO_MOD_ENABLED

async def setup(bot):
    await bot.add_cog(ModerationControl(bot))
