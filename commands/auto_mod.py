import discord
from discord.ext import commands
from openai import OpenAI
from config import OPENAI_API_KEY
from commands.ai import ModerationControl

client = OpenAI(api_key=OPENAI_API_KEY)

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Système de modération automatique initialisé!")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignorer les messages des bots
        if message.author.bot:
            return

        # Vérifier si l'automod est activé
        automod_cog = self.bot.get_cog("ModerationControl")
        if not automod_cog or not automod_cog.is_auto_mod_enabled():
            return

        print(f"Message reçu de {message.author}: {message.content}")

        # Vérifier si le message est approprié
        try:
            response = client.moderations.create(
                input=message.content
            )
            
            # Debug: Afficher les résultats de la modération
            categories = response.results[0].categories
            print("Résultats de la modération:", categories)
            
            # Liste des raisons de modération
            reasons = []
            if categories.harassment:
                reasons.append("harcèlement")
            if categories.hate:
                reasons.append("contenu haineux")
            if categories.self_harm:
                reasons.append("automutilation")
            if categories.sexual:
                reasons.append("contenu sexuel")
            if categories.violence:
                reasons.append("violence")
            
            if reasons:
                print(f"Message inapproprié détecté de {message.author}")
                await message.delete()
                reason_text = ", ".join(reasons)
                await message.channel.send(
                    f"{message.author.mention}, votre message a été supprimé pour les raisons suivantes : {reason_text}.",
                    delete_after=10
                )
                
        except Exception as e:
            print(f"Erreur lors de la modération automatique : {e}")

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
