import discord
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv
from commands.ai import ModerationControl
import asyncio
import time

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moderated_messages = {}  
        self.bot.loop.create_task(self.cleanup_cache())  

    async def cleanup_cache(self):
        """Nettoie le cache toutes les 10 secondes"""
        while True:
            current_time = time.time()
            to_remove = []
            
            for message_hash, (timestamp, categories) in self.moderated_messages.items():
                if current_time - timestamp > 60:  
                    to_remove.append(message_hash)
            
            for message_hash in to_remove:
                del self.moderated_messages[message_hash]
            
            await asyncio.sleep(10)  

    def get_message_hash(self, content):
        """Crée un hash simple du contenu du message"""
        return hash(content.lower().strip())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        automod_cog = self.bot.get_cog("ModerationControl")
        if not automod_cog or not automod_cog.is_auto_mod_enabled():
            return

        antispam_cog = self.bot.get_cog("AntiSpam")
        if antispam_cog and antispam_cog.is_spam_message(message.id):
            print(f"[AUTOMOD] Message spam ignoré: {message.author.name}")
            return

        try:
            if not message.guild.me.guild_permissions.manage_messages:
                return

            
            message_hash = self.get_message_hash(message.content)
            current_time = time.time()
            
            if message_hash in self.moderated_messages:
                timestamp, detected_categories = self.moderated_messages[message_hash]
                if current_time - timestamp <= 60:  
                    result = "✅ OK" if not detected_categories else f"❌ ({', '.join(detected_categories)})"
                    print(f"[AUTOMOD CACHE] {message.author.name}: {message.content[:30]}{'...' if len(message.content) > 30 else ''} {result}")
                    
                    if detected_categories:
                        await message.delete()
                        await message.channel.send(
                            f"{message.author.mention}, votre message a été supprimé pour les raisons suivantes : {', '.join(detected_categories)}.",
                            delete_after=10
                        )
                    return

            response = client.moderations.create(
                input=message.content
            )
            
            categories = response.results[0].categories
            detected_categories = []
            if categories.harassment:
                detected_categories.append("harcèlement")
            if categories.hate:
                detected_categories.append("contenu haineux")
            if categories.self_harm:
                detected_categories.append("automutilation")
            if categories.sexual:
                detected_categories.append("contenu sexuel")
            if categories.violence:
                detected_categories.append("violence")
            
            
            self.moderated_messages[message_hash] = (current_time, detected_categories)
            
            result = "✅ OK" if not detected_categories else f"❌ ({', '.join(detected_categories)})"
            print(f"[AUTOMOD] {message.author.name}: {message.content[:30]}{'...' if len(message.content) > 30 else ''} {result}")
            
            if detected_categories:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, votre message a été supprimé pour les raisons suivantes : {', '.join(detected_categories)}.",
                    delete_after=10
                )
        except Exception as e:
            print(f"Erreur lors de la modération automatique : {e}")

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
