from datetime import datetime
from discord.ext import commands
from database.mysql_connection import connect_to_db  # Ajuster le chemin si nécessaire

class AddLeagueMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_league_match(self, ctx, club_id: int, club_position: int, opponent_club_ids: str, opponent_positions: str, opponent_forces: str, score: str, round_number: int):
        """Ajouter un match de ligue et enregistrer l'action dans l'historique"""
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Vérifier si les équipes existent
                opponent_club_ids = list(map(int, opponent_club_ids.split(',')))
                opponent_positions = list(map(int, opponent_positions.split(',')))
                opponent_forces = list(map(int, opponent_forces.split(',')))

                if len(opponent_club_ids) != 4 or len(opponent_positions) != 4 or len(opponent_forces) != 4:
                    await ctx.send("Vous devez fournir exactement 4 clubs adverses, 4 positions et 4 forces.")
                    return

                # Vérifier si la ligue existe
                cursor.execute("SELECT * FROM leagues WHERE league_id = %s", (club_id,))
                league_data = cursor.fetchone()

                if not league_data:
                    await ctx.send(f"La ligue avec l'ID {club_id} n'existe pas.")
                    return

                # Ajouter le match de ligue
                query = """
                INSERT INTO league_match (
                    club_id, club_position, 
                    opponent_club_id_1, opponent_club_id_2, opponent_club_id_3, opponent_club_id_4, 
                    opponent_force_1, opponent_force_2, opponent_force_3, opponent_force_4, 
                    position_1, position_2, position_3, position_4, 
                    score, round, start_date
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(query, (
                    club_id, club_position,
                    opponent_club_ids[0], opponent_club_ids[1], opponent_club_ids[2], opponent_club_ids[3],
                    opponent_forces[0], opponent_forces[1], opponent_forces[2], opponent_forces[3],
                    opponent_positions[0], opponent_positions[1], opponent_positions[2], opponent_positions[3],
                    score, round_number, start_date
                ))
                conn.commit()

                # Enregistrer l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                VALUES (%s, %s, %s, %s, %s)
                """
                action_details = f"Match entre {club_id} et les clubs {', '.join(map(str, opponent_club_ids))} avec le score {score} (Ligue: {club_id})"
                cursor.execute(history_query, ("league_match", club_id, "ajout", action_details, start_date))
                conn.commit()

                await ctx.send("Match de ligue ajouté avec succès.")
            except Exception as e:
                await ctx.send(f"Erreur lors de l'ajout : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Connexion à la base de données échouée.")

async def setup(bot):
    await bot.add_cog(AddLeagueMatch(bot))