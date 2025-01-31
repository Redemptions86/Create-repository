from discord.ext import commands

class AddUpdateForce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_update_force(self, ctx, target_type: str, target_id: int, force_value: int):
        """Ajoute ou met à jour la force d'un club ou d'un membre"""

        # Vérification du type de cible
        if target_type not in ["club", "member"]:
            await ctx.send("Le type de cible doit être 'club' ou 'member'.")
            return

        # Vérification que la force est un nombre entier positif
        if not isinstance(force_value, int) or force_value < 0:
            await ctx.send("La force doit être un entier positif.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Vérification de l'existence de l'ID (club ou membre)
                if target_type == "club":
                    cursor.execute(
                        "SELECT * FROM clubs WHERE club_id = %s", (target_id,))
                elif target_type == "member":
                    cursor.execute(
                        "SELECT * FROM members WHERE member_id = %s", (target_id,))

                if not cursor.fetchone():
                    await ctx.send(f"{target_type.capitalize()} avec l'ID {target_id} introuvable.")
                    return

                # Ajout ou mise à jour de la force dans la base de données
                if target_type == "club":
                    query = "INSERT INTO forces (club_id, force_value, date_recorded) VALUES (%s, %s, NOW()) ON DUPLICATE KEY UPDATE force_value = %s"
                    cursor.execute(query, (target_id, force_value, force_value))
                elif target_type == "member":
                    query = "INSERT INTO forces (member_id, force_value, date_recorded) VALUES (%s, %s, NOW()) ON DUPLICATE KEY UPDATE force_value = %s"
                    cursor.execute(query, (target_id, force_value, force_value))

                conn.commit()
                await ctx.send(f"Force du {target_type} avec ID {target_id} mise à jour à {force_value}.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la mise à jour de la force : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

async def setup(bot):
    await bot.add_cog(AddUpdateForce(bot))