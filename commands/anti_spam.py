import discord
from discord import app_commands
from discord.ext import commands
import time
from collections import defaultdict
from datetime import timedelta

GUILD_ID = 1293979587264380928
OWNER_ID = 829064566742057020

# Configuration anti-spam
SPAM_THRESHOLD = 5  # Nombre de messages
SPAM_WINDOW = 10  # Fenêtre de temps en secondes
MUTE_DURATION = 300  # Durée du mute en secondes (5 minutes)

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anti_spam_enabled = True
        self.message_history = defaultdict(list)
        self.warned_users = set()

    @app_commands.command(name="antispam", description="Active ou désactive l'anti-spam")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.describe(state="on ou off")
    async def antispam(self, interaction: discord.Interaction, state: str):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("Seulement Emgodrick peut exécuter cette commande", ephemeral=True)
            return

        if state.lower() == "on":
            self.anti_spam_enabled = True
            await interaction.response.send_message("Anti-spam activé.")
        elif state.lower() == "off":
            self.anti_spam_enabled = False
            await interaction.response.send_message("Anti-spam désactivé.")
        else:
            await interaction.response.send_message("Valeur invalide. Utilise 'on' ou 'off'.")

    def is_anti_spam_enabled(self):
        return self.anti_spam_enabled

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.anti_spam_enabled or message.author.bot:
            return

        current_time = time.time()
        user_id = message.author.id

        # Nettoyer l'historique des messages anciens
        self.message_history[user_id] = [
            msg_time for msg_time in self.message_history[user_id]
            if current_time - msg_time < SPAM_WINDOW
        ]

        # Ajouter le nouveau message
        self.message_history[user_id].append(current_time)

        # Vérifier si l'utilisateur spam
        if len(self.message_history[user_id]) >= SPAM_THRESHOLD:
            if user_id in self.warned_users:
                # Mute l'utilisateur
                try:
                    await message.author.timeout(discord.utils.utcnow() + timedelta(seconds=MUTE_DURATION), reason="Spam")
                    await message.channel.send(
                        f"{message.author.mention} a été mute pendant 5 minutes pour spam.",
                        delete_after=10
                    )
                    # Réinitialiser l'historique et l'avertissement
                    self.message_history[user_id] = []
                    self.warned_users.remove(user_id)
                except discord.Forbidden:
                    await message.channel.send("Je n'ai pas les permissions nécessaires pour mute cet utilisateur.")
            else:
                # Avertir l'utilisateur
                await message.channel.send(
                    f"{message.author.mention}, arrêtez de spammer ou vous serez mute pendant 5 minutes.",
                    delete_after=10
                )
                self.warned_users.add(user_id)

    @commands.Cog.listener()
    async def on_ready(self):
        automod_cog = self.bot.get_cog("ModerationControl")
        auto_mod_state = "Activé" if automod_cog and automod_cog.is_auto_mod_enabled() else "Désactivé"
        print(f"État de l'anti-spam: {'Activé' if self.anti_spam_enabled else 'Désactivé'} | AutoMod: {auto_mod_state}")

async def setup(bot):
    await bot.add_cog(AntiSpam(bot)) 