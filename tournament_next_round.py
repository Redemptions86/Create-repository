from discord.ext import commands
from bot import bot  # Assurez-vous que 'bot' est bien importé depuis le bon fichier
from datetime import datetime  # Importation de datetime pour la gestion de la date et de l'heure

class TournamentNextRound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tournament_next_round(self, ctx, tournament_id: int):
        """Démarrer le round suivant dans un match de tournoi"""
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Récupérer les informations actuelles du tournoi
                query = "SELECT round, start_date FROM tournaments WHERE tournament_id = %s AND status = 'active'"
                cursor.execute(query, (tournament_id,))
                result = cursor.fetchone()

                if result:
                    current_round, start_date = result
                    next_round = current_round + 1

                    # Mettre à jour le round et la date de début dans la table tournaments
                    update_query = "UPDATE tournaments SET round = %s, start_date = %s WHERE tournament_id = %s"
                    cursor.execute(update_query, (next_round, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), tournament_id))
                    conn.commit()

                    # Enregistrement de l'action dans l'historique
                    history_query = """
                    INSERT INTO history (entity_type, entity_id, action_type, action_details)
                    VALUES (%s, %s, %s, %s)
                    """
                    action_details = f"Round {next_round} du tournoi {tournament_id} a commencé."
                    cursor.execute(history_query, ("tournament_round", tournament_id, "démarrage", action_details))
                    conn.commit()

                    # Récupérer l'ID de l'historique
                    history_id = cursor.lastrowid

                    # Mettre à jour la table tournaments avec l'ID de l'historique
                    update_history_query = """
                    UPDATE tournaments
                    SET history_id = %s
                    WHERE tournament_id = %s
                    """
                    cursor.execute(update_history_query, (history_id, tournament_id))
                    conn.commit()

                    await ctx.send(f"Round {next_round} du tournoi {tournament_id} a commencé.")
                else:
                    await ctx.send(f"Le tournoi {tournament_id} n'est pas actif ou n'existe pas.")
            except Exception as e:
                await ctx.send(f"Erreur lors du démarrage du round : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

# Fonction setup pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(TournamentNextRound(bot))