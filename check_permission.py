import discord
from discord.ext import commands
from database import connect_to_db  # Assurez-vous que cette fonction est correctement importée

class CheckPermissionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def check_permission(self, ctx, discord_id: int, command_name: str):
        """Vérifier si un membre a la permission d'utiliser une commande"""
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Trouver l'ID de la commande
                cursor.execute(
                    "SELECT command_id FROM commands WHERE command_name = %s", (command_name,))
                command = cursor.fetchone()

                if command:
                    command_id = command[0]

                    # Trouver les rôles du membre
                    cursor.execute(
                        "SELECT role_id FROM member_roles WHERE member_id = (SELECT member_id FROM members WHERE discord_id = %s)",
                        (discord_id,))
                    roles = cursor.fetchall()

                    for role in roles:
                        role_id = role[0]

                        # Vérifier si le rôle a la permission d'utiliser la commande
                        cursor.execute(
                            "SELECT * FROM command_permissions WHERE command_id = %s AND role_id = %s",
                            (command_id, role_id))
                        permission = cursor.fetchone()

                        if permission:
                            await ctx.send(f"Le membre avec ID {discord_id} a la permission d'utiliser la commande `{command_name}`.")
                            return

                    await ctx.send(f"Le membre avec ID {discord_id} n'a pas la permission d'utiliser la commande `{command_name}`.")
                else:
                    await ctx.send(f"La commande `{command_name}` n'existe pas.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la vérification des permissions : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

# Fonction setup pour charger le cog
async def setup(bot):
    await bot.add_cog(CheckPermissionCog(bot))