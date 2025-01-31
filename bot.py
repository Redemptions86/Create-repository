import os
import tracemalloc
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database.mysql_connection import connect_to_db
import asyncio

# S'assurer que le répertoire de travail est correct
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Configuration du journal
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Charger les variables d'environnement
load_dotenv()

# Variables de configuration
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")

if not TOKEN:
    raise ValueError("Le jeton Discord (DISCORD_TOKEN) est manquant dans le fichier .env.")
if not PREFIX:
    logging.warning("Aucun préfixe spécifié. Utilisation du préfixe par défaut '!'.")

# Création des intents
INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.guilds = True
INTENTS.members = True
INTENTS.message_content = True

# Création du bot
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)

# Dossiers à explorer pour charger les fichiers Python
directories_to_search = ["cogs"]

# Charger les fichiers et autres cogs
async def load_files():
    """Charge les fichiers Python depuis les dossiers spécifiés, y compris les sous-dossiers."""
    loaded_files = []
    failed_files = []

    for directory in directories_to_search:
        folder_path = os.path.join(".", directory)

        if os.path.isdir(folder_path):
            for root, _, files in os.walk(folder_path):
                for filename in files:
                    if filename.endswith(".py") and filename != "__init__.py":
                        try:
                            relative_path = os.path.relpath(root, start=".")  # Chemin relatif
                            cog_path = f"{relative_path.replace(os.sep, '.')}.{filename[:-3]}"
                            
                            # Si le cog est déjà chargé, on le décharge avant de le recharger
                            if cog_path in bot.extensions:
                                await bot.unload_extension(cog_path)
                                logging.info(f"⚠️ Le cog {cog_path} a été déchargé pour être rechargé.")
                            
                            await bot.load_extension(cog_path)
                            logging.info(f"✅ Fichier chargé : {cog_path}")
                            loaded_files.append(cog_path)
                        except Exception as e:
                            logging.error(f"❌ Erreur lors du chargement du fichier {filename}: {e}")
                            failed_files.append(filename)

    if failed_files:
        logging.warning(f"⚠️ Certains fichiers n'ont pas été chargés : {', '.join(failed_files)}")
    else:
        logging.info("✅ Tous les fichiers sont opérationnels.")

    return loaded_files, failed_files


# Charger les extensions
async def load_extensions():
    extensions = [
        "database.botcommands",
        "database.club_forces_queries",
        "database.club_match_queries",
        "database.club_queries",
        "database.command_permissions_queries",
        "database.command_translation_queries",
        "database.commands_queries",
        "database.events_queries",
        "database.forces_queries",
        "database.history_queries",
        "database.league_match_queries",
        "database.member_roles_queries",
        "database.members_permissions_queries",
        "database.members_queries",
        "database.tournaments_queries",
        "database.tournaments_and_matches",
        "database.rankings_queries",
        "cogs.forces_management",
        "cogs.member_commands",
    ]

    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logging.info(f"✅ Extension '{ext}' chargée avec succès.")
        except Exception as e:
            logging.error(f"❌ Erreur lors du chargement de l'extension '{ext}': {e}")


# Événement de démarrage
@bot.event
async def on_ready():
    logging.info(f"{bot.user} est prêt et en ligne !")
    await load_extensions()  # Charger les extensions après que le bot soit prêt


# Démarrage du bot
async def main():
    await load_files()  # Charger les cogs avant de démarrer le bot
    await load_extensions()  # Charger les extensions spécifiques
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())  # Exécuter la coroutine main() correctement