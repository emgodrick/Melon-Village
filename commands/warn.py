import discord
from discord import app_commands
from discord.ext import commands
import asyncio

GUILD_ID = 1293979587264380928

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="warn",
        description="Avertit un utilisateur avec une raison et le mute pendant 5 minutes"
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        user="L'utilisateur à avertir",
        reason="La raison de l'avertissement"
    )
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        await user.timeout(discord.utils.utcnow() + discord.timedelta(minutes=5), reason=reason)
        
        await interaction.response.send_message(
            f"{user.mention} a été averti et mute pendant 5 minutes pour : **{reason}**"
        )

async def setup(bot):
    await bot.add_cog(Warn(bot))

