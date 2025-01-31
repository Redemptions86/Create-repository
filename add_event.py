from datetime import datetime
from discord.ext import commands
from database.mysql_connection import connect_to_db  # Assurez-vous que cette fonction est correctement importée

class AddEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_event(
            self, ctx, club_id: int, discord_id: int, total_points: int, start_date: str, end_date: str):
        """Ajouter un événement pour un club"""

        # Vérification des formats de date
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            await ctx.send("Les dates doivent être au format 'YYYY-MM-DD'.")
            return

        # Vérification que la date de fin est après la date de début
        if end_date_obj < start_date_obj:
            await ctx.send("La date de fin ne peut pas être avant la date de début.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Vérification de l'existence du club
                cursor.execute("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
                if not cursor.fetchone():
                    await ctx.send(f"Le club avec l'ID {club_id} n'existe pas.")
                    return

                # Ajouter un événement dans la table events
                query = """
                INSERT INTO events (club_id, discord_id, total_points, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (club_id, discord_id, total_points, start_date, end_date))
                conn.commit()

                # Enregistrement de l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                VALUES (%s, %s, %s, %s, %s)
                """
                action_details = f"Événement ajouté pour le club {club_id} avec Discord ID {discord_id} et {total_points} points (Du {start_date} au {end_date})."
                cursor.execute(history_query, ("event", club_id, "ajout", action_details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()

                await ctx.send(f"Événement ajouté avec succès pour le club {club_id}.")
            except Exception as e:
                await ctx.send(f"Erreur lors de l'ajout de l'événement : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

# Configuration du cog
async def setup(bot):
    await bot.add_cog(AddEvent(bot))