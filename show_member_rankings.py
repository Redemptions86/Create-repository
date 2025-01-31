@commands.command()
    async def show_member_rankings(self, ctx):
        """Affiche les forces des membres par ordre décroissant."""
        query = """
        SELECT m.pseudo, c.club_name, f.team1_force
        FROM members m
        JOIN clubs c ON m.club_id = c.club_id
        JOIN forces f ON m.member_id = f.member_id
        ORDER BY f.team1_force DESC
        """
        conn = connect_to_db()
        if not conn:
            await ctx.send("❌ Impossible de se connecter à la base de données.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rankings = cursor.fetchall()

            if not rankings:
                await ctx.send("Aucun membre trouvé.")
                return

            # Générer un message avec les forces des membres
            message = "**Classements des membres par force :**\n\n"
            for rank, member in enumerate(rankings, 1):
                message += f"**#{rank} {member[0]}** (Club : {member[1]}) | Force : {member[2]}\n"

            await ctx.send(message)
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de l'affichage des forces : {e}")
        finally:
            cursor.close()
            conn.close()