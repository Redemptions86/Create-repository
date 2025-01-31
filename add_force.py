import discord
from discord.ext import commands
from database.mysql_connection import execute_query
from database.club_forces_queries import add_club_force, get_club_force  # Import des fonctions

class ClubForceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="add_force")
    async def add_force(self, ctx: commands.Context, club_id: int, total_force: int):
        """Ajouter la force d'un club."""
        try:
            # Ajouter la force du club dans la base de données
            await add_club_force(club_id, total_force)
            await ctx.send(f"La force du club avec ID {club_id} a été mise à jour à {total_force}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout de la force du club : {e}")

    @commands.command(name="get_force")
    async def get_force(self, ctx: commands.Context, club_id: int):
        """Obtenir la force actuelle d'un club."""
        try:
            # Récupérer la force du club depuis la base de données
            result = await get_club_force(club_id)
            if result:
                total_force = result[0]['total_force']
                await ctx.send(f"La force actuelle du club avec ID {club_id} est de {total_force}.")
            else:
                await ctx.send(f"Le club avec l'ID {club_id} n'a pas de force enregistrée.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération de la force du club : {e}")

# Fonction pour ajouter le cog
async def setup(bot: commands.Bot):
    await bot.add_cog(ClubForceCog(bot))