from discord.ext import commands

class ShowForce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_force(self, ctx, target_type: str, target_id: int):
        """Affiche la force d'un club ou d'un membre"""
        if target_type not in ["club", "member"]:
            await ctx.send("Le type de cible doit être 'club' ou 'member'.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                if target_type == "club":
                    query = "SELECT force_value, date_recorded FROM forces WHERE club_id = %s ORDER BY date_recorded DESC LIMIT 1"
                    cursor.execute(query, (target_id,))
                elif target_type == "member":
                    query = "SELECT force_value, date_recorded FROM forces WHERE member_id = %s ORDER BY date_recorded DESC LIMIT 1"
                    cursor.execute(query, (target_id,))

                force_data = cursor.fetchone()

                if force_data:
                    await ctx.send(f"Force du {target_type} avec ID {target_id} : {force_data[0]} (enregistrée le {force_data[1]}).")
                else:
                    await ctx.send(f"Aucune force trouvée pour le {target_type} avec ID {target_id}.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la récupération de la force : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(ShowForce(bot))