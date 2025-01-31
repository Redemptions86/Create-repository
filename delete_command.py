import discord
from discord.ext import commands
from database.commands_queries import delete_command  # Importation de la fonction asynchrone de suppression

class CommandManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def delete_command(self, ctx, command_name: str):
        """Supprime une commande de la base de données"""
        try:
            # Utilisation de la fonction delete_command depuis commands_queries.py
            await delete_command(command_name)  # Attente de la fonction asynchrone
            await ctx.send(f"Commande '{command_name}' supprimée avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la suppression de la commande : {e}")

# Fonction setup pour charger le cog
async def setup(bot):
    await bot.add_cog(CommandManagementCog(bot))  # Ajout du cog de manière synchrone