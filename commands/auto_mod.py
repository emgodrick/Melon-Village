import discord
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv
from commands.ai import ModerationControl

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignorer les messages des bots
        if message.author.bot:
            return

        # Vérifier si l'automod est activé
        automod_cog = self.bot.get_cog("ModerationControl")
        if not automod_cog or not automod_cog.is_auto_mod_enabled():
            return

        # Vérifier si le message est approprié
        try:
            response = client.moderations.create(
                input=message.content
            )
            
            # Debug: Afficher les résultats de la modération
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
            print(f"Message de {message.author}: {message.content} {result}")
            
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
