from discord.ext import commands
from bot import bot  # Assurez-vous que 'bot' est bien importé depuis le bon fichier

class EliminateTournamentClub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eliminate_tournament_club(self, ctx, tournament_id: int, club_id: int):
        """Éliminer un club du tournoi"""
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Mettre à jour le statut du club à 'eliminated'
                update_query = "UPDATE tournaments SET status = 'eliminated' WHERE tournament_id = %s AND club_id = %s"
                cursor.execute(update_query, (tournament_id, club_id))
                conn.commit()

                # Enregistrement de l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details)
                VALUES (%s, %s, %s, %s)
                """
                action_details = f"Le club {club_id} a été éliminé du tournoi {tournament_id}."
                cursor.execute(
                    history_query,
                    ("tournament_match",
                     tournament_id,
                     "élimination",
                     action_details))
                conn.commit()

                # Récupérer l'ID de l'historique
                history_id = cursor.lastrowid

                # Mettre à jour le tournoi avec l'ID de l'historique
                update_history_query = """
                UPDATE tournaments
                SET history_id = %s
                WHERE tournament_id = %s AND club_id = %s
                """
                cursor.execute(
                    update_history_query,
                    (history_id,
                     tournament_id,
                     club_id))
                conn.commit()

                await ctx.send(f"Le club {club_id} a été éliminé du tournoi {tournament_id}.")
            except Exception as e:
                await ctx.send(f"Erreur lors de l'élimination du club du tournoi : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

# Fonction setup pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(EliminateTournamentClub(bot))