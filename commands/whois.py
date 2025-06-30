import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class Whois(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whois", description="Affiche les informations d'un joueur")
    @app_commands.checks.has_permissions(view_audit_log=True)
    @app_commands.describe(member="Le joueur dont vous voulez voir les informations")
    async def whois(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        embed = discord.Embed(title=f"Informations sur {member.name}", color=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)
        
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nom d'affichage", value=member.display_name, inline=True)
        embed.add_field(name="Compte créé le", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="A rejoint le serveur le", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
        
        roles = [role.mention for role in member.roles[1:]]  # Exclure @everyone
        roles_str = ", ".join(roles) if roles else "Aucun rôle"
        embed.add_field(name=f"Rôles [{len(roles)}]", value=roles_str, inline=False)
        
        status = str(member.status).capitalize()
        embed.add_field(name="Statut", value=status, inline=True)
        
        if member.activity:
            activity_type = str(member.activity.type).split('.')[-1].capitalize()
            embed.add_field(name="Activité", value=f"{activity_type}: {member.activity.name}", inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Whois(bot)) 