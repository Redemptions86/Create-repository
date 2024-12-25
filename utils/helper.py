import json
from discord.ext import commands

# Chargement des rôles depuis le fichier JSON
def load_roles():
    try:
        with open("config/roles.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Le fichier roles.json est introuvable.")
        return {}

# Vérifie si un utilisateur a un rôle spécifique
def has_role(member, role_name):
    return any(role.name == role_name for role in member.roles)

# Récupération du rôle requis pour une commande
def get_required_role(command_name):
    roles = load_roles()
    return roles.get(command_name)

# Vérifie si l'utilisateur a les permissions nécessaires
async def check_permissions(ctx, required_role):
    if required_role is None:
        return True  # Pas de rôle requis pour cette commande
    if has_role(ctx.author, required_role):
        return True
    await ctx.send(f"Vous n'avez pas le rôle requis : {required_role}")
    return False

# Simplifie l'envoi d'un message
async def send_message(channel, content):
    if channel is None:
        print("Canal introuvable.")
        return
    await channel.send(content)

# Chargement des canaux depuis le fichier JSON
def load_channels():
    try:
        with open("config/channels.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Le fichier channels.json est introuvable.")
        return {}

# Récupère un canal par son nom
def get_channel_by_name(guild, channel_name):
    return discord.utils.get(guild.channels, name=channel_name)