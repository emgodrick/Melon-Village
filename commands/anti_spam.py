import discord
from discord import app_commands
from discord.ext import commands
import time
from collections import defaultdict
from datetime import timedelta
import asyncio

GUILD_ID = 1293979587264380928
OWNER_ID = 829064566742057020

# Configuration anti-spam
SPAM_THRESHOLD = 5  # Nombre de messages
SPAM_WINDOW = 10  # Fenêtre de temps en secondes
MUTE_DURATION = 300  # Durée du mute en secondes 

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anti_spam_enabled = True
        self.message_history = defaultdict(list)
        self.warned_users = set()
        self.spam_messages = set()  
        self.processing_users = set()  

    @app_commands.command(name="antispam", description="Active ou désactive l'anti-spam")
    @app_commands.checks.has_permissions(administrator=True)
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

    def is_spam_message(self, message_id):
        """Vérifie si un message a été marqué comme spam"""
        return message_id in self.spam_messages

    def mark_as_spam(self, message_id):
        """Marque un message comme spam"""
        self.spam_messages.add(message_id)

    async def delete_spam_messages(self, channel, user_id, current_time):
        """Supprime les messages spam de manière optimisée"""
        if user_id in self.processing_users:
            return
        
        self.processing_users.add(user_id)
        
        try:
            messages_to_delete = []
            async for msg in channel.history(limit=100):
                if msg.author.id == user_id and current_time - msg.created_at.timestamp() < SPAM_WINDOW:
                    messages_to_delete.append(msg)
                    self.mark_as_spam(msg.id)
            
            if messages_to_delete:
                if len(messages_to_delete) <= 100:
                    try:
                        await channel.delete_messages(messages_to_delete)
                        print(f"[ANTI-SPAM] {len(messages_to_delete)} messages supprimés pour {user_id}")
                    except discord.HTTPException as e:
                        if e.status == 429:  
                            print(f"[ANTI-SPAM] Rate limit atteint, suppression différée pour {user_id}")
                            for msg in messages_to_delete:
                                try:
                                    await msg.delete()
                                    await asyncio.sleep(1)  
                                except:
                                    pass
                        else:
                            print(f"[ANTI-SPAM] Erreur lors de la suppression: {e}")
                else:
                    for i in range(0, len(messages_to_delete), 100):
                        batch = messages_to_delete[i:i+100]
                        try:
                            await channel.delete_messages(batch)
                            await asyncio.sleep(2)  
                        except discord.HTTPException:
                            for msg in batch:
                                try:
                                    await msg.delete()
                                    await asyncio.sleep(1)
                                except:
                                    pass
        except Exception as e:
            print(f"Erreur lors de la suppression des messages spam: {e}")
        finally:
            self.processing_users.discard(user_id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.anti_spam_enabled or message.author.bot:
            return

        current_time = time.time()
        user_id = message.author.id

        self.message_history[user_id] = [
            msg_time for msg_time in self.message_history[user_id]
            if current_time - msg_time < SPAM_WINDOW
        ]

        self.message_history[user_id].append(current_time)
        
        if len(self.message_history[user_id]) >= SPAM_THRESHOLD:
            self.mark_as_spam(message.id)
            
            await self.delete_spam_messages(message.channel, user_id, current_time)

            if user_id in self.warned_users:
                try:
                    await message.author.timeout(discord.utils.utcnow() + timedelta(seconds=MUTE_DURATION), reason="Spam")
                    await message.channel.send(
                        f"{message.author.mention} a été mute pendant 5 minutes pour spam. Tous ses messages spam ont été supprimés.",
                        delete_after=10
                    )

                    self.message_history[user_id] = []
                    self.warned_users.remove(user_id)
                except discord.Forbidden:
                    await message.channel.send("Je n'ai pas les permissions nécessaires pour mute cet utilisateur.")
            else:
                await message.channel.send(
                    f"{message.author.mention}, arrêtez de spammer ou vous serez mute pendant 5 minutes. Vos messages spam ont été supprimés.",
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