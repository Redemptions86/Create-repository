from discord.ext import commands
import aiomysql  # Assurez-vous d'importer aiomysql
from database.mysql_connection import connect_to_db  # Assurez-vous que l'import est correct

@commands.command()
async def list_roles(ctx):
    """Affiche la liste des rôles"""
    conn = None
    cursor = None
    try:
        # Connexion à la base de données en tant que coroutine
        conn = await connect_to_db()  # Utilisez 'await' ici pour appeler la coroutine
        if conn is None:
            raise Exception("Impossible de se connecter à la base de données.")

        async with conn.cursor() as cursor:  # Utilisez le contexte asynchrone pour le curseur
            await cursor.execute("SELECT role_id, role_name FROM member_roles")
            roles = await cursor.fetchall()

            if roles:
                message = "Liste des rôles :\n"
                for role in roles:
                    message += f"ID: {role[0]}, Rôle: {role[1]}\n"
                await ctx.send(message)
            else:
                await ctx.send("Aucun rôle trouvé.")
    except Exception as e:
        await ctx.send(f"Erreur lors de la récupération des rôles : {e}")
    finally:
        if conn:
            await conn.close()  # Fermez la connexion asynchrone

# Fonction setup pour enregistrer la commande
async def setup(bot):
    bot.add_command(list_roles)