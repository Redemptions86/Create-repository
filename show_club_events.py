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

class ShowClubEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_club_events(self, ctx, club_id: int):
        """Afficher tous les événements d'un club donné."""
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Vérification de l'existence du club
                cursor.execute("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
                club = cursor.fetchone()
                if not club:
                    await ctx.send(f"Le club avec l'ID {club_id} n'existe pas.")
                    return

                # Récupération des événements du club
                query = """
                SELECT event_id, discord_id, total_points, start_date, end_date
                FROM events
                WHERE club_id = %s
                """
                cursor.execute(query, (club_id,))
                events = cursor.fetchall()

                if not events:
                    await ctx.send(f"Aucun événement trouvé pour le club {club_id}.")
                    return

                # Construction du message à afficher
                event_list = "Événements pour le club ID {} :\n".format(club_id)
                for event in events:
                    event_list += (
                        f"- Événement ID: {event[0]}, Discord ID: {event[1]}, "
                        f"Points: {event[2]}, Début: {event[3]}, Fin: {event[4]}\n"
                    )

                await ctx.send(event_list)
            except Exception as e:
                await ctx.send(f"Erreur lors de la récupération des événements : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(ShowClubEvents(bot))