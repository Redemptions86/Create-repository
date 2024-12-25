from discord.ext import commands

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="show_ranking")
    async def show_ranking(self, ctx):
        """Affiche le classement."""
        await ctx.send("Voici le classement actuel : ...")

async def setup(bot):
    await bot.add_cog(Ranking(bot))