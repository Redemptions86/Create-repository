import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Connexion à la base de données MySQL avec les informations du fichier .env
def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Créer le bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Planificateur pour envoyer des messages
scheduler = AsyncIOScheduler()

# Fonction pour envoyer un message automatisé
async def send_scheduled_message(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)

# Ajouter un canal à la base de données
def add_channel_to_db(channel_id, channel_name, description=""):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO channels (channel_id, channel_name, description)
        VALUES (%s, %s, %s)
    """, (channel_id, channel_name, description))
    db.commit()
    db.close()

# Ajouter un message automatisé à la base de données
def add_auto_message(channel_id, message, interval_hours, interval_minutes):
    db = connect_to_db()
    cursor = db.cursor()
    start_date = datetime.now()
    cursor.execute("""
        INSERT INTO auto_messages (channel_id, message_content, interval_hours, interval_minutes, start_date, last_sent)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (channel_id, message, interval_hours, interval_minutes, start_date, start_date))
    db.commit()
    db.close()

# Récupérer les messages à envoyer
def get_auto_messages():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM auto_messages")
    messages = cursor.fetchall()
    db.close()
    return messages

# Commande pour ajouter un canal
@bot.command()
async def add_channel(ctx, channel_name: str, description: str = ""):
    """
    Ajouter un canal à la base de données.
    Syntaxe : !add_channel "Nom du canal" "Description"
    """
    add_channel_to_db(ctx.channel.id, channel_name, description)
    await ctx.send(f"Le canal {channel_name} a été ajouté à la base de données.")

# Commande pour démarrer l'envoi de messages automatisés
@bot.command()
async def start_auto_messages(ctx, interval_hours: int, interval_minutes: int, *messages):
    """
    Démarrer l'envoi de plusieurs messages automatisés à intervalles réguliers.
    Syntaxe : !start_auto_messages heures minutes message1 message2
    """
    if len(messages) == 0:
        await ctx.send("Erreur : Vous devez spécifier au moins un message.")
        return

    # Ajouter les messages à la base de données et planifier leur envoi
    for message in messages:
        add_auto_message(ctx.channel.id, message, interval_hours, interval_minutes)

        # Planifier l'envoi du message
        scheduler.add_job(
            send_scheduled_message,
            IntervalTrigger(hours=interval_hours, minutes=interval_minutes),
            args=[ctx.channel.id, message],
            name=f"auto_message_{ctx.channel.id}_{message}",
            replace_existing=True
        )

    # Démarrer le planificateur si ce n'est pas déjà fait
    if not scheduler.running:
        scheduler.start()

    await ctx.send(f"L'envoi automatisé de {len(messages)} message(s) a été démarré.")

# Commande pour modifier un message automatisé
@bot.command()
async def modify_auto_message(ctx, message_id: int, new_message: str):
    """
    Modifier un message automatisé déjà enregistré dans la base de données.
    Syntaxe : !modify_auto_message message_id "Nouveau message"
    """
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM auto_messages WHERE message_id = %s", (message_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute(
            "UPDATE auto_messages SET message_content = %s WHERE message_id = %s",
            (new_message, message_id))
        db.commit()
        db.close()

        # Supprimer l'ancien job et en créer un nouveau
        for job in scheduler.get_jobs():
            if job.name.endswith(f"_{message_id}"):
                job.remove()

        # Replanifier le message modifié
        cursor.execute(
            "SELECT * FROM auto_messages WHERE message_id = %s", (message_id,))
        updated_message = cursor.fetchone()
        scheduler.add_job(
            send_scheduled_message,
            IntervalTrigger(
                hours=updated_message[3],
                minutes=updated_message[4]),
            args=[updated_message[1], updated_message[2]],
            name=f"auto_message_{updated_message[1]}_{updated_message[2]}",
            replace_existing=True)

        await ctx.send(f"Le message avec ID {message_id} a été modifié.")
    else:
        db.close()
        await ctx.send(f"Aucun message trouvé avec l'ID {message_id}.")

# Commande pour supprimer un message automatisé
@bot.command()
async def delete_auto_message(ctx, message_id: int):
    """
    Supprimer un message automatisé de la base de données.
    Syntaxe : !delete_auto_message message_id
    """
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM auto_messages WHERE message_id = %s", (message_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute(
            "DELETE FROM auto_messages WHERE message_id = %s", (message_id,))
        db.commit()
        db.close()

        # Supprimer le job du planificateur
        for job in scheduler.get_jobs():
            if job.name.endswith(f"_{message_id}"):
                job.remove()

        await ctx.send(f"Le message avec ID {message_id} a été supprimé.")
    else:
        db.close()
        await ctx.send(f"Aucun message trouvé avec l'ID {message_id}.")

# Fonction setup pour l'enregistrement du cog
async def setup(bot):
    await bot.add_cog(AutoMessageCog(bot))

# Créer une classe pour le cog
class AutoMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot