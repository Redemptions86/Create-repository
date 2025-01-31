import discord
from discord.ext import commands
from database.mysql_connection import connect_to_db
from utils.format_table import format_as_table

class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @format_as_table(headers=["ID", "Pseudo", "Club ID", "Role ID"])
    async def list_members(self, ctx):
        """
        Liste les membres avec leur ID, pseudo, club_id et role_id.
        """
        try:
            # Utilisation de `async with` pour gérer la connexion à la base de données
            async with await connect_to_db() as conn:
                async with conn.cursor() as cursor:
                    # Exécuter la requête SQL
                    await cursor.execute("SELECT id, pseudo, club_id, role_id FROM members")
                    members = await cursor.fetchall()

                    if not members:
                        return []  # Aucun membre trouvé, retourne une liste vide

                    # Retourne les résultats sous forme de liste de tuples
                    return members

        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération des membres : {e}")
            return []

async def setup(bot):
    await bot.add_cog(MemberCommands(bot))
