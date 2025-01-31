# add_member.py

import discord
from discord.ext import commands
from database.mysql_connection import connect_to_db
from database.members_queries import add_member, member_exists

class AddMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_member(self, ctx, member: discord.Member, club_id: int = None):
        """Ajouter un nouveau membre à la base de données."""
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
                    await ctx.send(f"Le membre {pseudo} existe déjà dans la base de données.")
                    return

                # Ajouter le membre
                await add_member(cursor, discord_id, pseudo, club_id)
                await conn.commit()

                # Enregistrer l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details)
                VALUES (%s, %s, %s, %s)
                """
                action_details = f"Ajout du membre {pseudo} avec Discord ID {discord_id}."
                await cursor.execute(history_query, ("member", discord_id, "ajout", action_details))
                await conn.commit()

                club_message = f" et associé au club {club_id}" if club_id else ""
                await ctx.send(f"Membre {pseudo} ajouté avec succès{club_message}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout du membre : {e}")
        finally:
            if conn:
                await conn.close()