# delete_member.py

import discord
from discord.ext import commands
from database.mysql_connection import connect_to_db
from database.members_queries import delete_member, member_exists

class DeleteMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def delete_member(self, ctx, discord_id: int):
        """Supprimer un membre de la base de données"""
        conn = await connect_to_db()
        if not conn:
            await ctx.send("Impossible de se connecter à la base de données.")
            return

        try:
            async with conn.cursor() as cursor:
                # Vérifier si le membre existe
                member_data = await member_exists(cursor, discord_id)
                if not member_data:
                    await ctx.send(f"Aucun membre trouvé avec l'ID Discord {discord_id}.")
                    return

                # Supprimer le membre
                await delete_member(cursor, discord_id)
                await conn.commit()

                # Enregistrer l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details)
                VALUES (%s, %s, %s, %s)
                """
                action_details = f"Le membre avec ID {discord_id} a été supprimé de la base de données."
                await cursor.execute(history_query, ("member", discord_id, "suppression", action_details))
                await conn.commit()

                await ctx.send(f"Membre avec ID {discord_id} supprimé avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la suppression du membre : {e}")
        finally:
            if conn:
                await conn.close()