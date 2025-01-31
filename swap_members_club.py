import discord
from discord.ext import commands
from database.mysql_connection import connect_to_db

class SwapMembersClubCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def swap_members_club(self, ctx, member1: discord.Member, member2: discord.Member):
        """
        Échanger deux membres entre leurs clubs respectifs.
        """
        discord_id1 = member1.id
        discord_id2 = member2.id

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Récupérer les club_id des deux membres en une seule requête
                cursor.execute(""" 
                    SELECT discord_id, club_id FROM members WHERE discord_id IN (%s, %s)
                """, (discord_id1, discord_id2))
                members_data = cursor.fetchall()

                if len(members_data) != 2:
                    await ctx.send("L'un des membres n'existe pas dans la base de données.")
                    return

                # Extraire les données des membres
                member1_data = next((m for m in members_data if m[0] == discord_id1), None)
                member2_data = next((m for m in members_data if m[0] == discord_id2), None)

                if not member1_data or not member2_data:
                    await ctx.send("L'un des membres n'a pas été trouvé.")
                    return

                club_id1 = member1_data[1]
                club_id2 = member2_data[1]

                # Vérifier que les deux membres sont bien associés à des clubs
                if club_id1 is None or club_id2 is None:
                    await ctx.send("L'un des membres n'est pas associé à un club.")
                    return

                # Échanger les clubs des deux membres
                update_query = """
                    UPDATE members SET club_id = CASE
                        WHEN discord_id = %s THEN %s
                        WHEN discord_id = %s THEN %s
                    END WHERE discord_id IN (%s, %s)
                """
                cursor.execute(update_query, (discord_id1, club_id2, discord_id2, club_id1, discord_id1, discord_id2))
                conn.commit()

                # Enregistrer l'action dans l'historique
                action_details = f"Échange entre {member1.name} (Club {club_id1}) et {member2.name} (Club {club_id2})"
                history_query = """
                    INSERT INTO history (entity_type, entity_id, action_type, action_details)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(history_query, ("member", discord_id1, "échange de club", action_details))
                cursor.execute(history_query, ("member", discord_id2, "échange de club", action_details))
                conn.commit()

                await ctx.send(f"Échange effectué avec succès : {member1.name} ↔ {member2.name}.")
            except Exception as e:
                await ctx.send(f"Erreur lors de l'échange des membres : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(SwapMembersClubCommands(bot))