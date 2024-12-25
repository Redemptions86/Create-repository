from discord.ext import commands

class ClubManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_club")
    async def add_club(self, ctx, club_name: str):
        """Ajoute un club."""
        await ctx.send(f"Club '{club_name}' ajouté avec succès !")

async def setup(bot):
    await bot.add_cog(ClubManagement(bot))