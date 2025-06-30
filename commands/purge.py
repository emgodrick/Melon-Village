import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv('GUILD_ID', 0))

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Supprime les derniers messages d'un utilisateur.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.describe(
        user="L'utilisateur ciblé",
        amount="Nombre de messages à supprimer "
    )
    async def purge(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        amount: int
    ):
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Le nombre doit être entre 1 et 100.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        def is_user(m):
            return m.author.id == user.id

        deleted = await interaction.channel.purge(limit=amount, check=is_user)
        await interaction.followup.send(f"{len(deleted)} message(s) de {user.mention} supprimé(s).")

async def setup(bot):
    await bot.add_cog(Purge(bot))
