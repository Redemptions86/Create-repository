from datetime import datetime
from discord.ext import commands
from database.mysql_connection import connect_to_db  # Ajuster le chemin si nécessaire

class LeagueNextRound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def league_next_round(self, ctx, match_id: int, club_id: int, score: str, opponent_club_ids: str, opponent_forces: str, positions: str):
        """
        Démarrer le round suivant pour un match de ligue et mettre à jour toutes les informations du match.
        """
        try:
            team1_score, team2_score = map(int, score.split('-'))
            opponent_club_ids = list(map(int, opponent_club_ids.split(',')))  # Liste des IDs des clubs adverses
            opponent_forces = list(map(int, opponent_forces.split(',')))  # Liste des forces des adverses
            positions = list(map(int, positions.split(',')))  # Liste des positions
        except ValueError:
            await ctx.send("Format du score ou des informations invalides. Utilisez 'X-Y', 'id1,id2,id3,id4', 'force1,force2,force3,force4', 'pos1,pos2,pos3,pos4'.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM league_match WHERE match_id = %s", (match_id,))
                match = cursor.fetchone()

                if not match:
                    await ctx.send(f"Match ID {match_id} introuvable.")
                    return

                # Déterminer les nouvelles positions et rounds
                current_round = match[14] or 0
                new_round = current_round + 1

                # Mettre à jour toutes les informations pertinentes
                query = """
                UPDATE league_match
                SET round = %s, score = %s,
                    opponent_club_id_1 = %s, opponent_club_id_2 = %s, opponent_club_id_3 = %s, opponent_club_id_4 = %s,
                    opponent_force_1 = %s, opponent_force_2 = %s, opponent_force_3 = %s, opponent_force_4 = %s,
                    position_1 = %s, position_2 = %s, position_3 = %s, position_4 = %s
                WHERE match_id = %s
                """
                cursor.execute(query, (
                    new_round, score,
                    opponent_club_ids[0], opponent_club_ids[1], opponent_club_ids[2], opponent_club_ids[3],
                    opponent_forces[0], opponent_forces[1], opponent_forces[2], opponent_forces[3],
                    positions[0], positions[1], positions[2], positions[3],
                    match_id
                ))
                conn.commit()

                # Enregistrement de l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                VALUES (%s, %s, %s, %s, %s)
                """
                action_details = f"Round {new_round} démarré. Score mis à jour : {score}. Opponents : {opponent_club_ids}. Forces : {opponent_forces}. Positions : {positions}."
                cursor.execute(history_query, ("league_match", match_id, "round_start", action_details, datetime.now()))
                conn.commit()

                await ctx.send(f"Round {new_round} du match ID {match_id} démarré. Score : {score}. Opponents : {opponent_club_ids}. Forces : {opponent_forces}. Positions : {positions}.")
            except Exception as e:
                await ctx.send(f"Erreur : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Connexion à la base de données échouée.")

async def setup(bot):
    await bot.add_cog(LeagueNextRound(bot))