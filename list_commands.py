from discord.ext import commands
from database.mysql_connection import connect_to_db  # Assurez-vous que l'import est correct

@commands.command()
async def list_commands(ctx):
    """Affiche la liste des commandes avec leurs informations sous forme de tableau"""
    conn = None
    cursor = None
    try:
        # Connexion à la base de données
        conn = await connect_to_db()
        if conn is None:
            raise Exception("Impossible de se connecter à la base de données.")

        cursor = await conn.cursor()
        # Modifier la requête pour inclure la colonne 'utilisation'
        await cursor.execute("SELECT command_id, command_name, description, utilisation FROM commands")
        commands = await cursor.fetchall()

        if commands:
            # Créer l'en-tête du tableau
            message = "```\n"
            message += f"{'ID':<5} {'Commande':<20} {'Description':<40} {'Utilisation'}\n"
            message += "-" * 80 + "\n"  # Ligne de séparation

            # Ajouter les commandes sous forme de tableau
            for command in commands:
                message += f"{command[0]:<5} {command[1]:<20} {command[2]:<40} {command[3]}\n"

            message += "```"

            # Si le message dépasse 2000 caractères, le diviser
            while len(message) > 2000:
                await ctx.send(message[:2000])  # Envoyer les 2000 premiers caractères
                message = message[2000:]  # Réduire le message aux caractères restants

            # Envoyer le reste du message (moins de 2000 caractères)
            if message:
                await ctx.send(message)
        else:
            await ctx.send("Aucune commande trouvée.")
    except Exception as e:
        await ctx.send(f"Erreur lors de la récupération des commandes : {e}")
    finally:
        if cursor:
            await cursor.close()  # Assurez-vous de fermer le curseur asynchrone
        if conn:
            try:
                await conn.close()  # Fermer la connexion asynchrone seulement si elle est valide
            except Exception as close_error:
                print(f"Erreur lors de la fermeture de la connexion : {close_error}")

# Fonction setup pour enregistrer la commande
async def setup(bot):
    bot.add_command(list_commands)