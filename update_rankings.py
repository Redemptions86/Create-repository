import discord
from discord.ext import commands
from database.rankings_queries import get_all_rankings

class GetAllRankings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_all_rankings")
    async def get_all_rankings_command(self, ctx):
        """Affiche les classements de tous les clubs."""
        rankings = get_all_rankings()
        if rankings:
            rankings_list = "**Classements de tous les clubs :**\n"
            for rank in rankings:
                rankings_list += (
                    f"- **Club {rank[1]}** (ID : {rank[0]})\n"
                    f"  - Forces totales : {rank[2]}\n"
                    f"  - Matchs joués : {rank[3]}\n"
                    f"  - Victoires : {rank[4]}\n"
                    f"  - Défaites : {rank[5]}\n"
                    f"  - Points totaux : {rank[6]}\n"
                    f"  - Position : {rank[7]}\n\n"
                )
            await ctx.send(rankings_list)
        else:
            await ctx.send("Aucun classement disponible dans la base de données.")

async def setup(bot):
    await bot.add_cog(GetAllRankings(bot))