from discord.ext import commands

class CompareForces(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def compare_forces(self, ctx, *target_ids):
        """Compare les forces de plusieurs clubs ou membres"""
        if len(target_ids) < 2:
            await ctx.send("Veuillez spécifier au moins deux ID pour comparer.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                forces = []

                for target_id in target_ids:
                    query = """
                        SELECT target_type, force_value
                        FROM forces
                        WHERE (club_id = %s OR member_id = %s)
                        ORDER BY date_recorded DESC LIMIT 1
                    """
                    cursor.execute(query, (target_id, target_id))
                    force_data = cursor.fetchone()
                    if force_data:
                        forces.append((target_id, force_data[0], force_data[1]))

                if forces:
                    message = "Comparaison des forces :\n"
                    for force in forces:
                        message += f"{force[1]} ID: {force[0]} Force: {force[2]}\n"
                    await ctx.send(message)
                else:
                    await ctx.send("Aucune force trouvée pour les ID spécifiés.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la comparaison des forces : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(CompareForces(bot))