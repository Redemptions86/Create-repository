from discord.ext import commands
import os
import sys

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin_ids = [1244013791268835462, 1260798919059837018]

    @commands.command(name="restart")
    async def restart(self, ctx):
        """Redémarre le bot sans fermer Replit, uniquement pour les administrateurs."""
        if ctx.author.id not in self.admin_ids:
            await ctx.send("Désolé, vous n'avez pas la permission d'utiliser cette commande.")
            return
        await ctx.send("Redémarrage en cours...")
        os.execv(sys.executable, ['python'] + sys.argv)

async def setup(bot):
    await bot.add_cog(Admin(bot))