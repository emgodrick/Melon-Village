import discord
from discord import app_commands
from discord.ext import commands

GUILD_ID = 1293979587264380928
OWNER_ID = 829064566742057020

AUTO_MOD_ENABLED = True

class ModerationControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ensure_auto_mod_enabled()

    def ensure_auto_mod_enabled(self):
        global AUTO_MOD_ENABLED
        AUTO_MOD_ENABLED = True
        print("Modération automatique activée au démarrage")

    @app_commands.command(name="automod", description="Active ou désactive la modération automatique")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.describe(state="on ou off")
    async def automod(self, interaction: discord.Interaction, state: str):
        global AUTO_MOD_ENABLED

        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("Seulement Emgodrick peut exécuter cette commande", ephemeral=True)
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

    @commands.Cog.listener()
    async def on_ready(self):
        self.ensure_auto_mod_enabled()
        print(f"Bot connecté en tant que {self.bot.user.name}")
        print(f"État de la modération automatique: {'Activée' if AUTO_MOD_ENABLED else 'Désactivée'}")

async def setup(bot):
    await bot.add_cog(ModerationControl(bot))
