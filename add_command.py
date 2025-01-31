from discord.ext import commands
from database.commands_queries import add_command  # Importation de la fonction asynchrone d'ajout de commande

class CommandManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_command(self, ctx, command_name: str, description: str):
        """Ajouter une nouvelle commande"""
        try:
            # Utilisation de la fonction add_command depuis commands_queries.py
            await add_command(command_name, description)  # Attente de la fonction asynchrone
            await ctx.send(f"Commande '{command_name}' ajoutée avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout de la commande : {e}")

# Fonction setup pour charger le cog
async def setup(bot):
    await bot.add_cog(CommandManagementCog(bot))  # Ajout du cog de manière synchrone