import discord
from discord.ext import commands
from database.rankings_queries import get_ranking_by_club

class GetRanking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_ranking")
    async def get_ranking_command(self, ctx, club_id: int):
        """Affiche le classement d'un club spécifique."""
        ranking = get_ranking_by_club(club_id)
        if ranking:
            club_info = (
                f"**Classement du club {ranking[1]}**\n"
                f"- ID du club : {ranking[0]}\n"
                f"- Forces totales : {ranking[2]}\n"
                f"- Matchs joués : {ranking[3]}\n"
                f"- Victoires : {ranking[4]}\n"
                f"- Défaites : {ranking[5]}\n"
                f"- Points totaux : {ranking[6]}\n"
                f"- Position : {ranking[7]}"
            )
            await ctx.send(club_info)
        else:
            await ctx.send(f"Aucun classement trouvé pour le club avec l'ID {club_id}.")

async def setup(bot):
    await bot.add_cog(GetRanking(bot))