import discord
from discord.ext import commands
import json

class ForceManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forces = {}  # Stockage des forces des joueurs
        self.clubs = {}  # Stockage des forces par club

    def load_data(self):
        """Charge les données depuis un fichier JSON."""
        try:
            with open('forces_data.json', 'r') as f:
                data = json.load(f)
                self.forces = data.get('forces', {})
                self.clubs = data.get('clubs', {})
        except FileNotFoundError:
            pass  # Si le fichier n'existe pas encore, on ne fait rien

    def save_data(self):
        """Sauvegarde les données dans un fichier JSON."""
        data = {
            'forces': self.forces,
            'clubs': self.clubs
        }
        with open('forces_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    @commands.command(name="add_force_club")
    async def add_force_club(self, ctx, club_name: str, force1: int, force2: int):
        """Ajoute une force à un joueur dans un club, remplaçant l'ancienne si nécessaire."""
        if club_name not in self.clubs:
            self.clubs[club_name] = {}

        player = ctx.author.name  # Utilise le nom de l'utilisateur Discord comme nom du joueur

        if player not in self.clubs[club_name]:
            self.clubs[club_name][player] = []

        # Ajouter la nouvelle force
        self.clubs[club_name][player].append((force1, force2))

        # Trier et garder uniquement la force maximale (celle avec la plus grande somme)
        self.clubs[club_name][player] = sorted(
            self.clubs[club_name][player],
            key=lambda x: x[0] + x[1],
            reverse=True
        )[:1]  # Garde seulement la force la plus élevée

        self.save_data()  # Sauvegarde les données après modification
        await ctx.send(f"Force ajoutée pour {player} dans le club {club_name} : ({force1}, {force2}).")

    @commands.command(name="show_forces_club")
    async def show_forces_club(self, ctx, club_name: str):
        """Affiche toutes les forces enregistrées pour un club spécifique triées par ordre décroissant."""
        if club_name not in self.clubs:
            await ctx.send(f"Aucun club nommé {club_name} trouvé.")
            return

        forces_message = f"Forces enregistrées pour le club {club_name} :\n"

        # Trie les joueurs par la plus grande somme des forces
        sorted_club_forces = {}
        for player, forces in self.clubs[club_name].items():
            # Trie les forces pour chaque joueur en fonction de la somme décroissante (force1 + force2)
            sorted_forces = sorted(forces, key=lambda x: x[0] + x[1], reverse=True)
            sorted_club_forces[player] = sorted_forces

        # Génère le message trié pour chaque joueur
        for player, forces in sorted_club_forces.items():
            for force1, force2 in forces:
                forces_message += f"{player} : Team1 {force1} Team2 {force2}\n"

        await ctx.send(forces_message)

    @commands.command(name="show_all_clubs")
    async def show_all_clubs(self, ctx):
        """Affiche les forces de tous les clubs, triées par le joueur le plus fort."""
        if not self.clubs:
            await ctx.send("Aucun club enregistré.")
            return

        all_clubs = []
        for club_name, players in self.clubs.items():
            # Calcule la force maximale de chaque club
            max_force = max(max(player[0]) for player in players.values())
            all_clubs.append((club_name, max_force))

        # Trie les clubs par force maximale décroissante
        sorted_clubs = sorted(all_clubs, key=lambda x: x[1], reverse=True)

        # Génère le message
        clubs_message = "Classement des clubs par force maximale :\n"
        for club_name, max_force in sorted_clubs:
            clubs_message += f"{club_name} : Force max {max_force}\n"

        await ctx.send(clubs_message)

    @commands.command(name="show_match_data")
    async def show_match_data(self, ctx, match_type: str):
        """Affiche les données de league-match ou club-match en ordre chronologique."""
        if match_type not in ["league-match", "club-match"]:
            await ctx.send("Type de match invalide. Utilisez 'league-match' ou 'club-match'.")
            return

        try:
            with open(f"{match_type}_data.json", "r") as f:
                match_data = json.load(f)
        except FileNotFoundError:
            await ctx.send(f"Aucune donnée trouvée pour {match_type}.")
            return

        # Trier par date
        sorted_data = sorted(match_data, key=lambda x: x["date"])

        match_message = f"**Données pour {match_type}**\n"
        for entry in sorted_data:
            match_message += f"{entry['date']} : {entry['details']}\n"

        await ctx.send(match_message)

    def save_match_data(self, match_type, match_entry):
        """Sauvegarde les données pour league-match ou club-match."""
        try:
            with open(f"{match_type}_data.json", "r") as f:
                match_data = json.load(f)
        except FileNotFoundError:
            match_data = []

        match_data.append(match_entry)
        match_data = sorted(match_data, key=lambda x: x["date"])

        with open(f"{match_type}_data.json", "w") as f:
            json.dump(match_data, f, indent=4)

async def setup(bot):
    await bot.add_cog(ForceManagement(bot))