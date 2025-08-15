import discord
from discord import app_commands
from discord.ext import commands
import time
from collections import defaultdict
from datetime import timedelta
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv('GUILD_ID', 0))
OWNER_ID = int(os.getenv('OWNER_ID', 0))

SPAM_THRESHOLD = 5
SPAM_WINDOW = 10
MUTE_DURATION = 300

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
        return message_id in self.spam_messages

    def mark_as_spam(self, message_id):
        self.spam_messages.add(message_id)

    async def delete_spam_messages(self, channel, user_id, current_time):
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
                    except discord.HTTPException as e:
                        if e.status == 429:  
                            for msg in messages_to_delete:
                                try:
                                    await msg.delete()
                                    await asyncio.sleep(1)  
                                except:
                                    pass
                        else:
                            pass
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
            pass
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

async def setup(bot):
    await bot.add_cog(AntiSpam(bot)) 