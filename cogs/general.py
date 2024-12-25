from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="helps", aliases=["aides"])
    async def custom_helps(self, ctx):
        """Affiche l'aide personnalisée."""
        # On vérifie le préfixe utilisé dans la commande
        if "aides" in ctx.invoked_with:  # Si "aides" est utilisé, on affiche l'aide en français
            help_message_fr = """
            **Commandes disponibles :**
            - `/helps` ou `/aides` : Affiche cette aide.
            - `/hello` : Dit bonjour.
            - `/add_trusted_member <@membre>` : Ajoute un membre de confiance à la liste des membres autorisés à utiliser certaines commandes.
            - `/restart` : Redémarre le bot (admin uniquement).
            - `/add_club <nom_du_club>` : Ajoute un nouveau club.
            - `/add_member <nom_du_club> <nom_du_membre>` : Ajoute un membre à un club spécifique.
            - `/list_clubs` : Affiche tous les clubs enregistrés et leurs membres.
            - `/add_force <force1> <force2>` : Enregistre les forces des équipes en utilisant les pseudos des joueurs (team1 et team2).
            - `/add_force_club <club_name> <force1> <force2>` : Enregistre les forces sous un club spécifique.
            - `/clear_history_channel <channel_id>` : Efface l'historique des messages dans un canal spécifique en utilisant son ID.
            - `/clear_force_club <club_name>` : Efface toutes les forces enregistrées pour un club spécifique.
            - `/show_forces_club <club_name>` : Affiche les forces enregistrées pour un club spécifique, triées par ordre décroissant.
            """
            await ctx.send(help_message_fr)
        else:  # Sinon, c'est l'anglais
            help_message_en = """
            **Available Commands:**
            - `/helps` or `/aides` : Shows this help.
            - `/hello` : Says hello.
            - `/add_trusted_member <@member>` : Adds a trusted member to the list of members allowed to use certain commands.
            - `/restart` : Restarts the bot (admin only).
            - `/add_club <club_name>` : Adds a new club.
            - `/add_member <club_name> <member_name>` : Adds a member to a specific club.
            - `/list_clubs` : Shows all registered clubs and their members.
            - `/add_force <force1> <force2>` : Registers the forces of teams using player usernames (team1 and team2).
            - `/add_force_club <club_name> <force1> <force2>` : Registers forces under a specific club.
            - `/clear_history_channel <channel_id>` : Clears the message history in a specific channel using its ID.
            - `/clear_force_club <club_name>` : Clears all forces recorded for a specific club.
            - `/show_forces_club <club_name>` : Shows the forces recorded for a specific club, sorted in descending order.
            """
            await ctx.send(help_message_en)

    @commands.command(name="hello")
    async def hello(self, ctx):
        """Répond par un message de salutation."""
        await ctx.send("Hello! How can I assist you today?")

async def setup(bot):
    await bot.add_cog(General(bot))