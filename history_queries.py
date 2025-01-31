from discord.ext import commands
import logging
from datetime import datetime
from .mysql_connection import connect_to_db

# Fonction centralisée pour ajouter une entrée dans l'historique
async def add_history(entity_type, entity_id, action_type, action_details, discord_id, operation):
    """
    Enregistre une action dans l'historique.
    """
    query = """
    INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date, discord_id, operation)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    action_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Date actuelle
    conn = await connect_to_db()
    if conn:
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (
                        entity_type,
                        entity_id,
                        action_type,
                        action_details,
                        action_date,
                        discord_id,
                        operation,
                    )
                )
                await conn.commit()
                logging.info(
                    f"✅ Entrée ajoutée dans l'historique : {action_type} ({operation}) pour {entity_type} (ID: {entity_id}) par Discord ID: {discord_id}"
                )
        except Exception as e:
            logging.error(f"❌ Erreur lors de l'ajout dans l'historique : {e}")
        finally:
            conn.close()

class HistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_role")
    async def add_role(self, ctx, user: commands.MemberConverter, role: commands.RoleConverter):
        """Ajoute un rôle à un utilisateur et enregistre l'action dans l'historique."""
        await user.add_roles(role)
        # Appel de la fonction centralisée pour enregistrer l'historique
        await add_history(
            "role",
            role.id,
            "ajout",
            f"Ajout du rôle {role.name} à {user.name}",
            ctx.author.id,
            "ajout",
        )
        await ctx.send(f"Le rôle {role.name} a été ajouté à {user.name}.")

    @commands.command(name="add_club")
    async def add_club(self, ctx, club_name):
        """Ajoute un club et enregistre l'action dans l'historique."""
        # Simulation d'ajout de club dans la base de données
        club_id = 123  # ID fictif pour l'exemple
        # Appel de la fonction centralisée pour enregistrer l'historique
        await add_history(
            "club",
            club_id,
            "ajout",
            f"Ajout du club {club_name}",
            ctx.author.id,
            "ajout",
        )
        await ctx.send(f"Le club {club_name} a été ajouté avec succès.")

    @commands.command(name="get_history")
    async def get_history(self, ctx, discord_id):
        """Récupère l'historique d'un utilisateur."""
        query = "SELECT * FROM history WHERE discord_id = %s ORDER BY action_date DESC"
        conn = None

        try:
            conn = await connect_to_db()
            if conn:
                async with conn.cursor(dictionary=True) as cursor:
                    await cursor.execute(query, (discord_id,))
                    result = await cursor.fetchall()
                    logging.info(
                        f"✅ Historique récupéré pour Discord ID: {discord_id}, {len(result)} entrées trouvées."
                    )

                    # Formater la réponse pour être plus lisible
                    if result:
                        history_msg = "\n".join(
                            [
                                f"{entry['action_date']} - {entry['action_type']} ({entry['operation']}): {entry['action_details']}"
                                for entry in result
                            ]
                        )
                    else:
                        history_msg = "Aucune action trouvée dans l'historique."

                    await ctx.send(f"Historique pour {discord_id} :\n{history_msg}")
        except Exception as e:
            logging.error(
                f"❌ Erreur lors de la récupération de l'historique pour Discord ID {discord_id} : {e}"
            )
            await ctx.send("❌ Erreur lors de la récupération de l'historique.")
        finally:
            if conn:
                conn.close()


# Ajout du cog à l'extension
def setup(bot):
    bot.add_cog(HistoryCog(bot))
