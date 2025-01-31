from discord.ext import commands
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

class ShowEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_event(self, ctx, event_id: int):
        """Afficher les détails d'un événement spécifique."""
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Vérification de l'existence de l'événement
                query = "SELECT * FROM events WHERE event_id = %s"
                cursor.execute(query, (event_id,))
                event = cursor.fetchone()

                if not event:
                    await ctx.send(f"L'événement avec l'ID {event_id} n'existe pas.")
                    return

                # Construction du message à afficher
                event_details = (
                    f"**Détails de l'événement {event_id}** :\n"
                    f"- Club ID : {event[1]}\n"
                    f"- Discord ID : {event[2]}\n"
                    f"- Points totaux : {event[3]}\n"
                    f"- Date de début : {event[4]}\n"
                    f"- Date de fin : {event[5] if event[5] else 'Non terminé'}"
                )
                await ctx.send(event_details)
            except Exception as e:
                await ctx.send(f"Erreur lors de la récupération de l'événement : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(ShowEvent(bot))