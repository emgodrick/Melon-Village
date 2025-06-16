import discord
from discord import app_commands
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unban", description="Débannir un utilisateur du serveur")
    @app_commands.describe(
        user_id="L'ID de l'utilisateur à débannir",
        reason="La raison du débannissement"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(
        self,
        interaction: discord.Interaction,
        user_id: str,
        reason: str = "Aucune raison fournie"
    ):
        try:
            # Vérifier si l'ID est valide
            user_id = int(user_id)
        except ValueError:
            await interaction.response.send_message(
                "L'ID fourni n'est pas valide. Veuillez fournir un ID numérique.",
                ephemeral=True
            )
            return

        try:
            # Récupérer l'utilisateur banni
            user = await self.bot.fetch_user(user_id)
            
            # Vérifier si l'utilisateur est banni
            bans = [entry async for entry in interaction.guild.bans()]
            if not any(ban.user.id == user_id for ban in bans):
                await interaction.response.send_message(
                    "Cet utilisateur n'est pas banni du serveur.",
                    ephemeral=True
                )
                return

            # Débannir l'utilisateur
            await interaction.guild.unban(
                user,
                reason=f"Débanni par {interaction.user}: {reason}"
            )

            embed = discord.Embed(
                title="Utilisateur débanni",
                color=discord.Color.green()
            )
            embed.add_field(name="Utilisateur", value=f"{user.name} ({user.id})", inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            await interaction.response.send_message(embed=embed)

        except discord.NotFound:
            await interaction.response.send_message(
                "Utilisateur non trouvé. Vérifiez l'ID fourni.",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Je n'ai pas les permissions nécessaires pour débannir cet utilisateur.",
                ephemeral=True
            )
        except discord.HTTPException:
            await interaction.response.send_message(
                "Une erreur s'est produite lors du débannissement de l'utilisateur.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Unban(bot)) 