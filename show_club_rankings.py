@commands.command()
    async def show_club_rankings(self, ctx, order_by: str = "points"):
        """
        Affiche les classements des clubs.
        Arguments :
        - points : Classement par points (par défaut).
        - forces : Classement par forces.
        - wins : Classement par victoires.
        """
        valid_orders = {"points": "total_points", "forces": "total_forces", "wins": "total_wins"}
        if order_by not in valid_orders:
            await ctx.send("❌ Critère de tri invalide. Utilisez : points, forces ou wins.")
            return

        query = f"""
        SELECT club_name, total_points, total_wins, total_forces
        FROM rankings
        ORDER BY {valid_orders[order_by]} DESC
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
                await ctx.send("Aucun classement trouvé.")
                return

            # Générer un message avec les classements
            message = "**Classements des clubs :**\n\n"
            for rank, club in enumerate(rankings, 1):
                message += f"**#{rank} {club[0]}** | Points : {club[1]} | Victoires : {club[2]} | Forces : {club[3]}\n"

            await ctx.send(message)
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de l'affichage des classements : {e}")
        finally:
            cursor.close()
            conn.close()