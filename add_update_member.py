# add_update_member.py

import discord
from discord.ext import commands
from database.mysql_connection import connect_to_db
from database.members_queries import add_member, update_member, member_exists

class AddUpdateMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_update_member(self, ctx, member: discord.Member, club_id: int = None):
        """Ajouter ou mettre à jour un membre dans la base de données."""
        discord_id = member.id
        pseudo = member.name

        try:
            conn = await connect_to_db()
            if not conn:
                await ctx.send("Impossible de se connecter à la base de données.")
                return

            async with conn.cursor() as cursor:
                # Vérifier si le membre existe déjà
                existing_member = await member_exists(cursor, discord_id)
                
                if existing_member:
                    # Si le membre existe déjà, on le met à jour
                    await update_member(cursor, discord_id, pseudo)
                    action_type = "mise à jour"
                    action_details = f"Mise à jour du membre {pseudo} avec Discord ID {discord_id}."
                    await ctx.send(f"Membre {pseudo} mis à jour avec succès.")
                else:
                    # Sinon, on ajoute le membre
                    await add_member(cursor, discord_id, pseudo, club_id)
                    action_type = "ajout"
                    action_details = f"Ajout du membre {pseudo} avec Discord ID {discord_id}."

                # Enregistrer l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details)
                VALUES (%s, %s, %s, %s)
                """
                await cursor.execute(history_query, ("member", discord_id, action_type, action_details))
                await conn.commit()

        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout ou de la mise à jour du membre : {e}")
        finally:
            if conn:
                await conn.close()