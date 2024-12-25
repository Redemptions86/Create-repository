import discord
from discord.ext import commands
import os
import json
import asyncio
from utils.keep_alive import keep_alive  # Importation de la fonction pour garder le bot actif

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    print("Commandes disponibles :")
    for command in bot.commands:
        print(f"- {command.name}")
    print("Prêt à recevoir des commandes !")

# Charger les cogs automatiquement
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            if cog_name not in bot.extensions:
                try:
                    await bot.load_extension(cog_name)
                    print(f"Cog {filename} chargé.")
                except Exception as e:
                    print(f"Erreur lors du chargement de {filename} : {e}")
            else:
                print(f"Cog {filename} déjà chargé.")

@bot.command(name="reload")
@commands.has_permissions(administrator=True)
async def reload(ctx):
    """Recharge tous les cogs sans redémarrer le bot."""
    await load_cogs()
    await ctx.send("Toutes les extensions ont été rechargées.")

# Démarrage du bot et démarrage de Flask pour le rendre actif
def start_bot():
    keep_alive()  # Garde le bot actif via Flask
    with open("config/config.json") as f:
        config = json.load(f)
    try:
        bot.run(config["token"])  # Utilise la méthode bot.run pour démarrer le bot
    except Exception as e:
        print(f"Erreur lors du démarrage du bot : {e}")

start_bot()  # Démarre le bot et le serveur Flask pour maintenir l'activité
