from discord.ext import commands
from datetime import datetime
from database.club_match_queries import get_club_match, update_club_match  # Importation des fonctions
from database.history_queries import add_history  # Importer une fonction pour enregistrer dans l'historique

class ClubMatchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="end_club_match")
    async def end_club_match(self, ctx, match_id: int):
        """
        Termine un match de club en enregistrant la date de fin et en mettant à jour l'état du match.
        """
        try:
            # Vérifier si le match existe
            match = await get_club_match(match_id)

            if not match:
                await ctx.send(f"⚠️ Match avec l'ID {match_id} introuvable.")
                return

            # Vérifier si le match est déjà terminé
            if match.get('end_date'):  # Assurez-vous que le champ 'end_date' existe
                await ctx.send(f"⚠️ Le match ID {match_id} est déjà terminé.")
                return

            # Mettre à jour la date de fin
            end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await update_club_match(match_id, end_date=end_date)

            # Ajouter l'action à l'historique
            await add_history(
                entity_type="club_match",
                entity_id=match_id,
                action_type="fin",
                action_details=f"Match terminé avec l'ID {match_id}. Date de fin : {end_date}.",
                discord_id=ctx.author.id,
                operation="modification",
            )

            await ctx.send(f"✅ Match ID {match_id} terminé avec succès. Date de fin : {end_date}.")
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de la fin du match : {e}")

# Fonction setup pour ajouter le Cog
async def setup(bot):
    # Utilisez un mécanisme pour éviter de recharger plusieurs fois le même Cog
    if bot.get_cog("ClubMatchCog") is None:
        await bot.add_cog(ClubMatchCog(bot))
