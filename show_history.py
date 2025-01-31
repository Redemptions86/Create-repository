# show_history.py

from bot import bot, connect_to_db
from datetime import datetime
from discord.ext import commands

class ShowHistory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_history(self, ctx, *club_ids: int):
        """
        Afficher l'historique des matchs et événements pour plusieurs clubs.
        Utilisation : !show_history <club_id1> <club_id2> ...
        """
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Récupérer l'historique pour les clubs spécifiés
                club_ids_placeholder = ", ".join(["%s"] * len(club_ids))

                # Historique des matchs de club
                query_club_matches = f"""
                SELECT club_id, opponent_club_id, score, match_type, timestamp
                FROM club_match
                WHERE club_id IN ({club_ids_placeholder})
                ORDER BY timestamp DESC
                """
                cursor.execute(query_club_matches, club_ids)
                club_matches = cursor.fetchall()

                # Historique des matchs de ligue
                query_league_matches = f"""
                SELECT league_id, team1_id, team2_id, score, timestamp
                FROM league_match
                WHERE team1_id IN ({club_ids_placeholder}) OR team2_id IN ({club_ids_placeholder})
                ORDER BY timestamp DESC
                """
                cursor.execute(query_league_matches, club_ids * 2)  # Utiliser deux fois club_ids pour les deux colonnes
                league_matches = cursor.fetchall()

                # Historique des tournois
                query_tournaments = f"""
                SELECT name, tournament_date, club_id
                FROM tournaments
                WHERE club_id IN ({club_ids_placeholder})
                ORDER BY tournament_date DESC
                """
                cursor.execute(query_tournaments, club_ids)
                tournaments = cursor.fetchall()

                # Construire le message
                history_message = "**Historique des clubs sélectionnés :**\n\n"

                # Ajouter les matchs de club
                history_message += "**Matchs de club :**\n"
                for match in club_matches:
                    history_message += (
                        f"Club {match[0]} vs Club {match[1]} | Score: {match[2]} | Type: {match[3]} | Date: {match[4]}\n")

                # Ajouter les matchs de ligue
                history_message += "\n**Matchs de ligue :**\n"
                for match in league_matches:
                    history_message += (
                        f"Ligue {match[0]}: {match[1]} vs {match[2]} | Score: {match[3]} | Date: {match[4]}\n")

                # Ajouter les tournois
                history_message += "\n**Tournois :**\n"
                for tournament in tournaments:
                    history_message += (
                        f"Tournoi: {tournament[0]} | Club: {tournament[2]} | Date: {tournament[1]}\n")

                await ctx.send(history_message if history_message else "Aucun historique trouvé pour les clubs sélectionnés.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la récupération de l'historique : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

# Correction : rendre la fonction setup asynchrone
async def setup(bot):
    await bot.add_cog(ShowHistory(bot))