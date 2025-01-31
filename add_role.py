import discord
from discord.ext import commands
from database.mysql_connection import connect_to_db

class AddRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_role(self, ctx, discord_id: int, role_name: str):
        """Ajouter un rôle à un membre"""
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Vérifier si le membre existe
                cursor.execute(
                    "SELECT member_id FROM members WHERE discord_id = %s", (discord_id,))
                member = cursor.fetchone()
                if not member:
                    await ctx.send(f"Le membre avec l'ID Discord {discord_id} n'existe pas.")
                    return

                member_id = member[0]

                # Vérifier si le rôle existe
                cursor.execute(
                    "SELECT role_id FROM roles WHERE role_name = %s", (role_name,))
                role = cursor.fetchone()
                if not role:
                    await ctx.send(f"Le rôle '{role_name}' n'existe pas.")
                    return

                role_id = role[0]

                # Vérifier si le membre a déjà ce rôle
                cursor.execute(
                    "SELECT 1 FROM member_roles WHERE member_id = %s AND role_id = %s", (member_id, role_id))
                if cursor.fetchone():
                    await ctx.send(f"Le membre {discord_id} a déjà le rôle '{role_name}'.")
                    return

                # Ajouter le rôle au membre
                query = "INSERT INTO member_roles (member_id, role_id) VALUES (%s, %s)"
                cursor.execute(query, (member_id, role_id))
                conn.commit()
                await ctx.send(f"Rôle '{role_name}' ajouté avec succès au membre {discord_id}.")
            except Exception as e:
                await ctx.send(f"Erreur lors de l'ajout du rôle : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

# Fonction setup pour charger le cog
async def setup(bot):
    await bot.add_cog(AddRoleCog(bot))