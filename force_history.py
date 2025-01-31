from discord.ext import commands

class ForceHistory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def force_history(self, ctx, target_type: str, target_id: int):
        """Affiche l'historique des forces d'un club ou d'un membre"""

        # Vérification du type de cible
        if target_type not in ["club", "member"]:
            await ctx.send("Le type de cible doit être 'club' ou 'member'.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Vérification de l'existence de l'ID (club ou membre)
                if target_type == "club":
                    cursor.execute(
                        "SELECT * FROM clubs WHERE club_id = %s", (target_id,))
                elif target_type == "member":
                    cursor.execute(
                        "SELECT * FROM members WHERE member_id = %s", (target_id,))

                if not cursor.fetchone():
                    await ctx.send(f"{target_type.capitalize()} avec l'ID {target_id} introuvable.")
                    return

                # Récupérer l'historique des forces
                if target_type == "club":
                    query = "SELECT force_value, date_recorded FROM forces WHERE club_id = %s ORDER BY date_recorded DESC LIMIT 5"
                    cursor.execute(query, (target_id,))
                elif target_type == "member":
                    query = "SELECT force_value, date_recorded FROM forces WHERE member_id = %s ORDER BY date_recorded DESC LIMIT 5"
                    cursor.execute(query, (target_id,))

                force_history = cursor.fetchall()

                if force_history:
                    message = f"Historique des forces du {target_type} avec ID {target_id} :\n"
                    for record in force_history:
                        # Formatage de la date pour une meilleure lisibilité
                        formatted_date = record[1].strftime('%d-%m-%Y %H:%M:%S')
                        message += f"Force: {record[0]} (enregistrée le {formatted_date})\n"
                    await ctx.send(message)
                else:
                    await ctx.send(f"Aucun historique de force trouvé pour le {target_type} avec ID {target_id}.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la récupération de l'historique des forces : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(ForceHistory(bot))