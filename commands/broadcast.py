import discord
from discord import app_commands
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv('GUILD_ID', 0))
OWNER_ID = int(os.getenv('OWNER_ID', 0))

# Configuration OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class Broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="broadcast", description="Génère un message d'annonce formaté avec l'IA")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.describe(
        message="Le message ou sujet de l'annonce à transformer",
        channel="Le salon où envoyer l'annonce (optionnel)"
    )
    async def broadcast(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        # Vérifier que c'est le propriétaire du bot
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("Seulement Emgodrick peut exécuter cette commande", ephemeral=True)
            return

        # Vérifier si la clé API OpenAI est configurée
        if not client.api_key:
            await interaction.response.send_message("Erreur: Clé API OpenAI non configurée.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        try:
            # Préparer le prompt pour OpenAI
            prompt = f"""Tu es un assistant qui aide à créer des annonces Discord formatées et professionnelles. 
            
            Transforme le message suivant en une annonce Discord avec du formatage :
            
            "{message}"
            
            Règles à suivre :
            - Commence toujours par un titre principal en gras avec un emoji : **🎯 Titre Principal**
            - Ajoute des sous-titres en italique : *📋 Sous-titre*
            - Utilise des citations avec > pour les informations importantes
            - Utilise le formatage Discord : **gras**, *italique*, __souligné__, ~~barré~~, `code`
            - Sois informatif, créatif et engageant
            - N'ajoute pas de questions comme "que puis-je faire d'autre"
            - Garde le message structuré avec des sections claires
            - Utilise des emojis appropriés pour chaque section
            - Termine par un appel à l'action positif
            
            Exemple de structure :
            **🎯 Titre Principal**
            
            *📋 Contexte*
            > Information importante en citation
            
            *💡 Suggestions*
            - Point 1
            - Point 2
            
            *🎉 Conclusion*
            Message de fin motivant
            
            Réponds uniquement avec le message formaté, sans explications supplémentaires."""

            # Appel à l'API OpenAI avec la nouvelle syntaxe
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un assistant spécialisé dans la création d'annonces Discord formatées avec du markdown. Tu dois toujours créer des messages structurés avec des titres, sous-titres et citations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.8
            )

            generated_message = response.choices[0].message.content.strip()

            # Déterminer le salon de destination
            target_channel = channel or interaction.channel

            # Envoyer le message formaté
            await target_channel.send(generated_message)
            await interaction.followup.send(f"✅ Message envoyé dans {target_channel.mention} !", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"❌ Erreur: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Broadcast(bot)) 