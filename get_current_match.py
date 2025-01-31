from discord.ext import commands
from database.league_match_queries import get_league_matches_in_progress  # Importer la fonction de requêtes de matchs de ligue
from database.tournaments_queries import get_tournaments_in_progress  # Importer la fonction de requêtes de tournois

class GetCurrentMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_current_match(self, ctx):
        """
        Récupérer les matchs en cours dans les tables de ligue et de tournois.
        """
        try:
            # Récupérer les matchs en cours dans la table league_match
            league_matches = await get_league_matches_in_progress()

            # Récupérer les matchs en cours dans la table tournaments
            tournament_matches = await get_tournaments_in_progress()

            # Vérifier si des matchs sont en cours et les afficher
            if league_matches or tournament_matches:
                message = "Matchs en cours :\n"
                if league_matches:
                    message += "\n**League Matches :**\n"
                    for match in league_matches:
                        message += f"Match ID {match[0]} - League Match {match[1]} vs {match[2]} {match[3]}\n"

                if tournament_matches:
                    message += "\n**Tournament Matches :**\n"
                    for match in tournament_matches:
                        message += f"Match ID {match[0]} - Tournament Match {match[1]} vs {match[2]} {match[3]}\n"

                await ctx.send(message)
            else:
                await ctx.send("Aucun match en cours pour le moment.")

        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération des matchs : {e}")

# Fonction setup pour ajouter le Cog de manière asynchrone
async def setup(bot):
    if not bot.get_cog("GetCurrentMatch"):
        await bot.add_cog(GetCurrentMatch(bot))
    else:
        print("Cog 'GetCurrentMatch' déjà chargé.")