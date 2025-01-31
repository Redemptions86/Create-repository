from datetime import datetime
from discord.ext import commands
from database.mysql_connection import connect_to_db  # Ajuster le chemin si nécessaire

class EndRound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def end_round(self, ctx, match_id: int, score: str):
        """
        Terminer un round d'un match de ligue, mettre à jour le score, les positions des clubs et les forces des adversaires.
        """
        try:
            team1_score, team2_score = map(int, score.split('-'))
        except ValueError:
            await ctx.send("Le format du score est invalide. Utilisez le format 'X-Y'.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Vérifier si le match existe
                cursor.execute("SELECT * FROM league_match WHERE match_id = %s", (match_id,))
                match_data = cursor.fetchone()

                if not match_data:
                    await ctx.send(f"Aucun match trouvé avec l'ID {match_id}.")
                    return

                # Récupérer les données des clubs et adversaires
                club_id = match_data[1]  # club_id du match
                club_position = match_data[2]  # position actuelle du club principal
                opponent_club_ids = match_data[3:7]  # opponent_club_id_1 à opponent_club_id_4
                opponent_forces = match_data[7:11]  # opponent_force_1 à opponent_force_4
                positions = match_data[11:15]  # position_1 à position_4

                # Calculer la nouvelle position du club principal
                new_club_position = 1 if team1_score > team2_score else 2

                # Mettre à jour le score du match et la date de fin
                end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = """
                UPDATE league_match
                SET score = %s, end_date = %s, round = round + 1
                WHERE match_id = %s
                """
                cursor.execute(query, (score, end_date, match_id))

                # Mettre à jour la position du club principal
                position_update_query = """
                UPDATE league_match
                SET club_position = %s
                WHERE match_id = %s
                """
                cursor.execute(position_update_query, (new_club_position, match_id))

                # Mettre à jour les positions des clubs adverses
                for i, position in enumerate(positions):
                    opponent_position_query = """
                    UPDATE league_match
                    SET position_%s = %s
                    WHERE match_id = %s
                    """
                    cursor.execute(opponent_position_query, (i+1, position, match_id))

                # Mettre à jour les forces des adversaires (si nécessaire)
                for i, force in enumerate(opponent_forces):
                    opponent_force_query = """
                    UPDATE league_match
                    SET opponent_force_%s = %s
                    WHERE match_id = %s
                    """
                    cursor.execute(opponent_force_query, (i+1, force, match_id))

                conn.commit()

                # Enregistrer l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                VALUES (%s, %s, %s, %s, %s)
                """
                action_details = f"Round terminé pour le match ID {match_id} avec le score {score}."
                cursor.execute(history_query, ("league_match", match_id, "end_round", action_details, end_date))
                conn.commit()

                await ctx.send(f"Round terminé pour le match ID {match_id} avec le score {score}.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la fin du round : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

# Fonction setup asynchrone pour charger le cog
async def setup(bot):
    await bot.add_cog(EndRound(bot))