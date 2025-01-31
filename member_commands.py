from discord.ext import commands

class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Commande simple pour saluer l'utilisateur"""
        await ctx.send("Hello, how can I help you today?")

    @commands.command()
    async def goodbye(self, ctx):
        """Commande simple pour dire au revoir"""
        await ctx.send("Goodbye! Have a great day!")

def setup(bot):
    bot.add_cog(MemberCommands(bot))