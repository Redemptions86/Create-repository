from discord.ext import commands
from datetime import datetime
from database.mysql_connection import connect_to_db

class ClubMatchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def update_match_score(self, ctx, match_id: int, new_score: str = None, new_opponent_scores: str = None):
        """
        Mettre à jour les scores d'un match de club.
        - Met à jour le score du club principal et/ou des clubs adverses.
        """
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Vérifier si le match existe
                cursor.execute("SELECT * FROM club_match WHERE match_id = %s", (match_id,))
                match = cursor.fetchone()

                if match:
                    # Vérifier si le match est déjà terminé
                    if match[5]:  # Supposons que la colonne 5 est 'end_date'
                        await ctx.send(f"Le match ID {match_id} est déjà terminé et ne peut pas être modifié.")
                        return

                    # Préparer la mise à jour des scores
                    updated = False

                    # Mettre à jour le score du club principal
                    if new_score:
                        query = "UPDATE club_match SET club_score = %s WHERE match_id = %s"
                        cursor.execute(query, (new_score, match_id))
                        updated = True

                    # Mettre à jour les scores des clubs adverses
                    if new_opponent_scores:
                        opponent_scores = new_opponent_scores.split(',')
                        if len(opponent_scores) == 4:
                            query = """
                            UPDATE club_match
                            SET opponent_club_1_score = %s, opponent_club_2_score = %s, opponent_club_3_score = %s, opponent_club_4_score = %s
                            WHERE match_id = %s
                            """
                            cursor.execute(query, (*opponent_scores, match_id))
                            updated = True
                        else:
                            await ctx.send("Veuillez fournir exactement 4 scores pour les clubs adverses.")
                            return

                    if updated:
                        conn.commit()

                        # Enregistrement de l'action dans l'historique
                        history_query = """
                        INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        action_details = f"Match avec l'ID {match_id} modifié. Nouveau score : {new_score}, Scores adverses : {new_opponent_scores}."
                        cursor.execute(
                            history_query,
                            ("club_match", match_id, "modification", action_details, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        )
                        conn.commit()

                        await ctx.send(f"Match ID {match_id} modifié avec succès.")
                    else:
                        await ctx.send("Aucune information n'a été modifiée.")
                else:
                    await ctx.send(f"Match avec l'ID {match_id} introuvable.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la modification du match : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

# Fonction setup pour ajouter le Cog de manière asynchrone
async def setup(bot):
    # Vérifier si le cog est déjà chargé
    if not bot.get_cog("ClubMatchCog"):
        await bot.add_cog(ClubMatchCog(bot))
    else:
        print("Cog 'ClubMatchCog' déjà chargé.")