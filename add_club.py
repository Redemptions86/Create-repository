import discord
from discord.ext import commands
from database.botcommands import add_club_with_validation
from database.history_queries import add_history  # Pour ajouter à l'historique

class AddClub(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def add_club(self, ctx: commands.Context, club_name: str):
        """Ajouter un club avec vérification de doublon et validation des données."""
        try:
            # Appel à la fonction SQL pour validation et ajout
            validation_message = add_club_with_validation(club_name)

            # Vérifie si la validation a retourné une erreur
            if "existe déjà" in validation_message or "ne peuvent pas être vides" in validation_message:
                await ctx.send(validation_message)
                return

            # Enregistrer l'action dans l'historique
            discord_id = ctx.author.id  # ID Discord de l'utilisateur ayant effectué l'action
            entity_type = "club"
            entity_id = club_name  # Nom du club utilisé comme identifiant
            action_type = "ajout"
            action_details = f"Ajout du club '{club_name}'"
            add_history(
                entity_type,
                entity_id,
                action_type,
                action_details,
                discord_id
            )

            # Confirmation de l'ajout
            await ctx.send(f"Le club '{club_name}' a été ajouté avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout du club : {e}")

# Configuration pour charger le cog dans le bot
async def setup(bot: commands.Bot):
    await bot.add_cog(AddClub(bot))