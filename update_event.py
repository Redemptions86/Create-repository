from discord.ext import commands
from datetime import datetime
import mysql.connector

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="votre_hôte",
            user="votre_utilisateur",
            password="votre_mot_de_passe",
            database="votre_base_de_données"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données : {err}")
        return None

class UpdateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def update_event(
        self, 
        ctx, 
        event_id: int, 
        total_points: int = None, 
        start_date: str = None, 
        end_date: str = None
    ):
        """Mettre à jour les informations d'un événement."""
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Vérification de l'existence de l'événement
                cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
                event = cursor.fetchone()
                if not event:
                    await ctx.send(f"L'événement avec l'ID {event_id} n'existe pas.")
                    return

                # Préparer la requête de mise à jour
                update_query = "UPDATE events SET "
                params = []
                if total_points is not None:
                    update_query += "total_points = %s, "
                    params.append(total_points)
                if start_date is not None:
                    try:
                        datetime.strptime(start_date, "%Y-%m-%d")
                        update_query += "start_date = %s, "
                        params.append(start_date)
                    except ValueError:
                        await ctx.send("La date de début doit être au format 'YYYY-MM-DD'.")
                        return
                if end_date is not None:
                    try:
                        datetime.strptime(end_date, "%Y-%m-%d")
                        update_query += "end_date = %s, "
                        params.append(end_date)
                    except ValueError:
                        await ctx.send("La date de fin doit être au format 'YYYY-MM-DD'.")
                        return

                # Vérifier si des champs ont été modifiés
                if not params:
                    await ctx.send("Aucun champ à mettre à jour.")
                    return

                # Finaliser la requête
                update_query = update_query.rstrip(", ") + " WHERE event_id = %s"
                params.append(event_id)

                # Exécuter la mise à jour
                cursor.execute(update_query, tuple(params))
                conn.commit()

                # Enregistrement dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                VALUES (%s, %s, %s, %s, %s)
                """
                action_details = f"Mise à jour de l'événement {event_id} : {', '.join([f'{key} = {value}' for key, value in zip(['total_points', 'start_date', 'end_date'], params[:-1])])}."
                cursor.execute(history_query, ("event", event_id, "modification", action_details, datetime.now()))
                conn.commit()

                await ctx.send(f"L'événement {event_id} a été mis à jour avec succès.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la mise à jour de l'événement : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(UpdateEvent(bot))