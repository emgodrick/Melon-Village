import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="timeout", description="Met un utilisateur en timeout")
    @app_commands.describe(
        user="L'utilisateur à mettre en timeout",
        duration="La durée du timeout en minutes (1-40320)",
        reason="La raison du timeout"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        duration: int,
        reason: str = "Aucune raison fournie"
    ):
        if duration < 1 or duration > 40320:
            await interaction.response.send_message(
                "La durée maximale autorisée par Discord est de 28 jours",
                ephemeral=True
            )
            return

        if user.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "Tu ne peux pas mettre en timeout quelqu'un qui a un rôle supérieur ou égal au tien.",
                ephemeral=True
            )
            return

        timeout_duration = timedelta(minutes=duration)
        await user.timeout(timeout_duration, reason=reason)

        embed = discord.Embed(
            title="Timeout appliqué",
            color=discord.Color.red()
        )
        embed.add_field(name="Utilisateur", value=user.mention, inline=True)
        embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
        embed.add_field(name="Durée", value=f"{duration} minutes", inline=True)
        embed.add_field(name="Raison", value=reason, inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Timeout(bot)) 