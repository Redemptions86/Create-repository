import discord
from discord.ext import commands
from database.history_queries import add_history  # Pour enregistrer dans l'historique
from database.club_queries import get_club_by_id, update_club  # Assurez-vous que ces fonctions existent

class ClubManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def add_mod_club(self, ctx, club_id: int, new_club_name: str):
        """Modifier un club et enregistrer l'action dans l'historique."""
        try:
            # Vérifie si le club existe avant de tenter la mise à jour
            result, error = await get_club_by_id(ctx, club_id)
            if error:
                await ctx.send(error)
                return

            if result:
                # Validation du nouveau nom du club
                if not new_club_name.strip():
                    await ctx.send("Le nom du club ne peut pas être vide.")
                    return

                # Mise à jour du club avec le nouveau nom
                await update_club(ctx, club_id, new_club_name)

                # Enregistrement de l'action dans l'historique
                discord_id = ctx.author.id  # ID Discord de l'utilisateur ayant effectué l'action
                entity_type = "club"
                entity_id = club_id  # Utilisation de l'ID du club
                action_type = "modification"
                action_details = f"Modification du club {club_id} : Nouveau nom = {new_club_name}"
                await add_history(ctx, entity_type, entity_id, action_type, action_details, discord_id)

                await ctx.send(f"Le club '{new_club_name}' (ID: {club_id}) a été mis à jour avec succès.")
            else:
                await ctx.send(f"Club avec ID {club_id} introuvable.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la mise à jour du club : {e}")

# Configuration pour charger le cog dans le bot
async def setup(bot: commands.Bot):
    await bot.add_cog(ClubManagement(bot))