import discord
from discord.ext import commands
import os
import json
import asyncio

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
            if cog_name not in bot.extensions:  # Vérifie si le cog est déjà chargé
                try:
                    await bot.load_extension(cog_name)
                    print(f"Cog {filename} chargé.")
                except Exception as e:
                    print(f"Erreur lors du chargement de {filename} : {e}")
            else:
                print(f"Cog {filename} déjà chargé.")

# Commande pour recharger les cogs
@bot.command(name="reload")
@commands.has_permissions(administrator=True)
async def reload(ctx):
    """Recharge tous les cogs sans redémarrer le bot."""
    await load_cogs()
    await ctx.send("Toutes les extensions ont été rechargées.")

# Démarrage du bot
async def main():
    await load_cogs()
    with open("config/config.json") as f:
        config = json.load(f)
    try:
        await bot.start(config["token"])  # Token sécurisé dans config.json
    except Exception as e:
        print(f"Erreur lors du démarrage du bot : {e}")
    finally:
        await bot.close()

asyncio.run(main())