import discord
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv
from commands.ai import ModerationControl

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        automod_cog = self.bot.get_cog("ModerationControl")
        if not automod_cog or not automod_cog.is_auto_mod_enabled():
            return

        try:
            if not message.guild.me.guild_permissions.manage_messages:
                return

            if message.author.guild_permissions.administrator:
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
