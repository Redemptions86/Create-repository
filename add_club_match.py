from discord.ext import commands
from datetime import datetime
from database.mysql_connection import execute_query  # Utilisation de la version asynchrone de execute_query

class ClubMatchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_club_match(self, ctx, club_id: int, opponent1_id: int, opponent1_strength: int, 
                             opponent2_id: int, opponent2_strength: int, opponent3_id: int, 
                             opponent3_strength: int, opponent4_id: int, opponent4_strength: int):
        """
        Ajouter un match de club contre 4 clubs adverses avec leur force.
        """
        try:
            # Vérifie si le club principal existe
            query = "SELECT * FROM clubs WHERE club_id = %s"
            club = await execute_query(query, (club_id,))

            if not club:
                await ctx.send(f"Le club avec l'ID {club_id} n'a pas été trouvé.")
                return

            # Liste des clubs adverses et leurs forces
            opponents = [
                (opponent1_id, opponent1_strength),
                (opponent2_id, opponent2_strength),
                (opponent3_id, opponent3_strength),
                (opponent4_id, opponent4_strength)
            ]

            opponent_details = []

            for opponent_id, strength in opponents:
                # Vérifier chaque club adverse et obtenir sa force
                opponent_query = "SELECT * FROM clubs WHERE club_id = %s"
                opponent = await execute_query(opponent_query, (opponent_id,))
                
                if not opponent:
                    await ctx.send(f"Le club adverse avec l'ID {opponent_id} n'a pas été trouvé.")
                    return
                opponent_details.append((opponent[0], opponent[1], strength))  # (ID, Nom, Force)

            # Ajouter le match de club dans la table club_match
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insertion dans la table club_match
            query = """
            INSERT INTO club_match (club_id, opponent_club_1, opponent_club_2, opponent_club_3, opponent_club_4, 
                                    start_date, opponent_club_1_strength, opponent_club_2_strength, 
                                    opponent_club_3_strength, opponent_club_4_strength)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            opponent_strengths = [opponent[2] for opponent in opponent_details]  # Liste des forces des adversaires

            await execute_query(query, (club_id, opponent_details[0][0], opponent_details[1][0], opponent_details[2][0], opponent_details[3][0], created_at,
                                  opponent_strengths[0], opponent_strengths[1], opponent_strengths[2], opponent_strengths[3]))

            # Enregistrement de l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            action_details = f"Match de club ajouté entre {club[1]} ({club_id}) et les clubs adverses avec les forces respectives {opponent_strengths}"
            await execute_query(history_query, ("club_match", club_id, "ajout", action_details, created_at))

            await ctx.send(f"Match de club ajouté avec succès contre les clubs adverses.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout des matchs de club : {e}")

# Utilisation de await pour charger le cog correctement
async def setup(bot):
    await bot.add_cog(ClubMatchCog(bot))