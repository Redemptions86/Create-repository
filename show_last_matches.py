import discord
from discord.ext import commands
from database.mysql_connection import connect_to_db

class ShowLastMatches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_last_matches(self, ctx, club_id: int):
        """Afficher les trois derniers matchs d'un club (matchs de club et de ligue)"""
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Récupérer les trois derniers matchs de club
                query_club = "SELECT * FROM club_match WHERE club_id = %s ORDER BY timestamp DESC LIMIT 3"
                cursor.execute(query_club, (club_id,))
                club_matches = cursor.fetchall()

                # Récupérer les trois derniers matchs de ligue
                query_league = "SELECT * FROM league_match WHERE team1_id = %s OR team2_id = %s ORDER BY timestamp DESC LIMIT 3"
                cursor.execute(query_league, (club_id, club_id))
                league_matches = cursor.fetchall()

                matches_message = f"Les trois derniers matchs du club {club_id} :\n\n"

                # Affichage des matchs de club
                if club_matches:
                    matches_message += "**Matchs de club :**\n"
                    for match in club_matches:
                        matches_message += f"Match ID: {match[0]} | Score: {match[3]} | Date: {match[4]}\n"
                else:
                    matches_message += "Aucun match de club trouvé.\n"

                # Affichage des matchs de ligue
                if league_matches:
                    matches_message += "\n**Matchs de ligue :**\n"
                    for match in league_matches:
                        matches_message += f"Match ID: {match[0]} | Score: {match[3]} | Date: {match[4]}\n"
                else:
                    matches_message += "Aucun match de ligue trouvé.\n"

                await ctx.send(matches_message)
            except Exception as e:
                await ctx.send(f"Erreur lors de l'affichage des derniers matchs : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(ShowLastMatches(bot))