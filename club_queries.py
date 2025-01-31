from database.mysql_connection import execute_query, connect_to_db
from mysql.connector import Error
from discord.ext import commands

async def execute_query(query, params=None, fetchone=False):
    """Exécute une requête SQL et gère la connexion et les erreurs."""
    try:
        connection, cursor = connect_to_db()
        if connection is None or cursor is None:
            return None, "Erreur de connexion à la base de données."

        cursor.execute(query, params or ())
        if fetchone:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        connection.commit()
        return result, None
    except Error as e:
        return None, f"Erreur MySQL : {e}"
    except Exception as e:
        return None, f"Erreur générale : {e}"
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Fonction déplacée en dehors de la classe
async def get_club_by_id(club_id):
    """Récupère un club par son ID."""
    query = "SELECT * FROM clubs WHERE club_id = %s"
    result, error = execute_query(query, (club_id,), fetchone=True)
    if error:
        return None, error
    return result, None

# Fonction déplacée en dehors de la classe
async def update_club(club_id, new_club_name, new_club_owner):
    """Met à jour un club dans la base de données."""
    if not new_club_name.strip() or not new_club_owner.strip():
        return "Le nom du club et le nom du propriétaire ne peuvent pas être vides."

    # Vérifier si le club existe
    query = "SELECT * FROM clubs WHERE club_id = %s"
    result, error = execute_query(query, (club_id,), fetchone=True)

    if error:
        return error

    if not result:
        return f"Aucun club trouvé avec l'ID '{club_id}'."

    query = "UPDATE clubs SET club_name = %s, club_owner = %s WHERE club_id = %s"
    result, error = execute_query(query, (new_club_name, new_club_owner, club_id))

    if error:
        return error
    else:
        return f"Le club avec ID '{club_id}' a été mis à jour."

class ClubManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_club_by_name")
    async def get_club_by_name(self, ctx, club_name):
        """Récupère un club par son nom."""
        query = "SELECT * FROM clubs WHERE club_name = %s"
        result, error = execute_query(query, (club_name,), fetchone=True)

        if error:
            await ctx.send(error)
            return

        if result:
            await ctx.send(f"Club trouvé :\nNom: {result[1]}\nPropriétaire: {result[2]}\nID: {result[0]}")
        else:
            await ctx.send(f"Aucun club trouvé avec le nom '{club_name}'.")

    @commands.command(name="add_club")
    async def add_club(self, ctx, club_name, club_owner):
        """Ajoute un club dans la base de données."""
        if not club_name.strip() or not club_owner.strip():
            await ctx.send("Le nom du club et le nom du propriétaire ne peuvent pas être vides.")
            return

        # Vérification de doublon
        query = "SELECT * FROM clubs WHERE club_name = %s"
        result, error = execute_query(query, (club_name,), fetchone=True)

        if error:
            await ctx.send(error)
            return

        if result:
            await ctx.send(f"Un club avec le nom '{club_name}' existe déjà.")
            return

        query = "INSERT INTO clubs (club_name, club_owner) VALUES (%s, %s)"
        result, error = execute_query(query, (club_name, club_owner))

        if error:
            await ctx.send(error)
        else:
            await ctx.send(f"Le club '{club_name}' a été ajouté avec succès.")

    @commands.command(name="update_club")
    async def update_club_command(self, ctx, club_id, new_club_name, new_club_owner):
        """Met à jour un club dans la base de données via la commande Discord."""
        message = update_club(club_id, new_club_name, new_club_owner)
        await ctx.send(message)

    @commands.command(name="delete_club")
    async def delete_club(self, ctx, club_id):
        """Supprime un club de la base de données."""
        query = "DELETE FROM clubs WHERE club_id = %s"
        result, error = execute_query(query, (club_id,))

        if error:
            await ctx.send(error)
        else:
            await ctx.send(f"Le club avec ID '{club_id}' a été supprimé.")

    @commands.command(name="list_clubs")
    async def list_clubs(self, ctx):
        """Récupère la liste de tous les clubs."""
        query = "SELECT club_id, club_name, points FROM clubs"
        result, error = execute_query(query)

        if error:
            await ctx.send(error)
            return

        if result:
            clubs_list = "\n".join([f"ID: {club[0]} | Nom: {club[1]} | Points: {club[2]}" for club in result])
            await ctx.send(f"Liste des clubs :\n{clubs_list}")
        else:
            await ctx.send("Aucun club trouvé.")

async def setup(bot):
    if "ClubManagementCog" not in bot.cogs:
        await bot.add_cog(ClubManagementCog(bot))