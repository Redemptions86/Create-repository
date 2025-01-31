import discord
from discord.ext import commands
from database.mysql_connection import connect_to_db

class AddMemberClub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_member_club(self, ctx, member: discord.Member, club_id: int):
        """
        Ajouter un membre existant à un club.
        """
        discord_id = member.id

        conn = connect_to_db()
        if not conn:
            await ctx.send("Impossible de se connecter à la base de données.")
            return

        try:
            cursor = conn.cursor()

            # Vérifier si le membre existe
            cursor.execute("SELECT * FROM members WHERE discord_id = %s", (discord_id,))
            member_data = cursor.fetchone()
            if not member_data:
                await ctx.send(f"Le membre {member.name} n'existe pas dans la base de données.")
                return

            # Vérifier si le club existe
            cursor.execute("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
            club_data = cursor.fetchone()
            if not club_data:
                await ctx.send(f"Le club avec ID {club_id} n'existe pas.")
                return

            # Mettre à jour le club_id du membre
            update_query = "UPDATE members SET club_id = %s WHERE discord_id = %s"
            cursor.execute(update_query, (club_id, discord_id))
            conn.commit()

            if cursor.rowcount == 0:
                await ctx.send(f"❌ Aucune mise à jour effectuée pour le membre {member.name}.")
                return

            # Enregistrer l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details)
            VALUES (%s, %s, %s, %s)
            """
            action_details = f"Le membre {member.name} a été ajouté au club {club_id}."
            cursor.execute(history_query, ("member", discord_id, "ajout au club", action_details))
            conn.commit()

            await ctx.send(f"Le membre {member.name} a été associé au club {club_id} avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'attribution du club : {e}")
        finally:
            cursor.close()
            conn.close()


async def setup(bot):
    await bot.add_cog(AddMemberClub(bot))