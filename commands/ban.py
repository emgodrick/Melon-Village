import discord
from discord import app_commands
from discord.ext import commands

GUILD_ID = 1293979587264380928
class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Bannir un utilisateur")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.describe(
        user="L'utilisateur à bannir",
        reason="La raison du bannissement"
    )
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str):
        guild = interaction.guild
        member = guild.get_member(user.id)

        if member is None:
            await interaction.response.send_message("Utilisateur non trouvé dans ce serveur.", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"{member.mention} a été banni pour : {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("Permissions insuffisantes", ephemeral=True)
            await user.send(f"Vous avez été banni de Melon Village pour : {reason}")
        except Exception as e:
            await interaction.response.send_message(f"Erreur lors du bannissement : {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ban(bot))

