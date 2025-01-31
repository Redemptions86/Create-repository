# cogs/club_management/list_clubs.py

from discord.ext import commands
from database.mysql_connection import execute_query  # Assurez-vous que cette fonction existe

class ClubManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def list_clubs(self, ctx):
        """
        Liste tous les clubs.
        """
        query = "SELECT club_id, club_name FROM clubs"
        try:
            # Exécuter la requête pour obtenir les clubs
            rows = await execute_query(query)
            
            if rows:
                # Créer une table formatée avec les résultats
                table = "ID | Nom du Club\n" + "-"*30
                for row in rows:
                    table += f"\n{row[0]} | {row[1]}"
                
                # Envoyer la table dans le canal Discord
                await ctx.send(table)
            else:
                await ctx.send("Aucun club trouvé.")
        
        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération des clubs : {e}")

# Chargement du cog
async def setup(bot):
    await bot.add_cog(ClubManagementCog(bot))