from discord.ext import commands
import aiomysql
from database.mysql_connection import connect_to_db  # Assurez-vous que cette fonction est asynchrone

class AddUpdateCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_update_command(self, ctx, command_name: str, description: str, permission_level: str):
        """Ajoute ou met à jour une commande dans la base de données"""
        try:
            conn = await connect_to_db()  # Connexion asynchrone
            if conn:
                async with conn.cursor() as cursor:
                    query = """
                        INSERT INTO commands (command_name, description, permission_level)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE description = %s, permission_level = %s
                    """
                    await cursor.execute(
                        query,
                        (command_name,
                         description,
                         permission_level,
                         description,
                         permission_level)
                    )
                    await conn.commit()
                    await ctx.send(f"Commande '{command_name}' ajoutée ou mise à jour avec succès.")
            else:
                await ctx.send("Impossible de se connecter à la base de données.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout ou de la mise à jour de la commande : {e}")
        finally:
            if conn:
                conn.close()  # Fermeture de la connexion si elle est ouverte

# Fonction setup pour charger le cog
async def setup(bot):
    await bot.add_cog(AddUpdateCommandCog(bot))  # Ajout du cog de manière synchrone