import discord
from discord import app_commands
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Expulse un utilisateur du serveur")
    @app_commands.describe(
        user="L'utilisateur à expulser",
        reason="La raison de l'expulsion"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str = "Aucune raison fournie"
    ):
        if user.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "Tu ne peux pas expulser quelqu'un qui a un rôle supérieur ou égal au tien.",
                ephemeral=True
            )
            return

        if not user.kickable:
            await interaction.response.send_message(
                "Je ne peux pas expulser cet utilisateur. Vérifie que mon rôle est plus haut que celui de l'utilisateur.",
                ephemeral=True
            )
            return

        try:
            await user.kick(reason=f"Par {interaction.user}: {reason}")
            
            embed = discord.Embed(
                title="Utilisateur expulsé",
                color=discord.Color.orange()
            )
            embed.add_field(name="Utilisateur", value=user.mention, inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                "Je n'ai pas les permissions nécessaires pour expulser cet utilisateur.",
                ephemeral=True
            )
        except discord.HTTPException:
            await interaction.response.send_message(
                "Une erreur s'est produite lors de l'expulsion de l'utilisateur.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Kick(bot)) 