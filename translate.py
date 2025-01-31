from discord.ext import commands
from database.mysql_connection import connect_to_db

class TranslationCog(commands.Cog):
    """Cog pour gérer les traductions des commandes."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, command_name, language):
        """Commande pour obtenir la traduction d'une commande dans une langue donnée."""
        # Connexion à la base de données
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Récupérer l'ID de la commande
                cursor.execute(
                    "SELECT command_id FROM commands WHERE command_name = %s", (command_name,))
                command = cursor.fetchone()
                if command:
                    command_id = command[0]

                    # Récupérer la traduction de la commande
                    cursor.execute(
                        "SELECT translation_text FROM command_translations WHERE command_id = %s AND language = %s",
                        (command_id, language)
                    )
                    translation = cursor.fetchone()

                    if translation:
                        await ctx.send(f"Traduction de '{command_name}' en {language}: {translation[0]}")
                    else:
                        await ctx.send(f"Aucune traduction trouvée pour '{command_name}' en {language}.")
                else:
                    await ctx.send(f"Commande '{command_name}' non trouvée.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la récupération de la traduction : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(TranslationCog(bot))  # Charger le cog dans le bot