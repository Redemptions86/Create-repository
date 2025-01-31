@commands.command()
async def add_tournament_match(
        self,
        ctx,
        tournament_id: int,
        club_id: int,
        opponent_club_ids: list,
        opponent_forces: list,
        positions: list,
        score: str,
        round: int,
        status: str):
    """Ajouter un match de tournoi avec des détails complets."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Requête pour insérer le match dans la table tournaments
            query = """
            INSERT INTO tournaments (
                tournament_id, club_id, club_position, opponent_club_id_1, opponent_club_id_2,
                opponent_club_id_3, opponent_club_id_4, opponent_force_1, opponent_force_2,
                opponent_force_3, opponent_force_4, position_1, position_2, position_3, position_4,
                round, status, start_date, score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (tournament_id, club_id, positions[0], opponent_club_ids[0], opponent_club_ids[1],
                 opponent_club_ids[2], opponent_club_ids[3], opponent_forces[0], opponent_forces[1],
                 opponent_forces[2], opponent_forces[3], positions[1], positions[2], positions[3],
                 positions[4], round, status, start_date, score)
            )
            conn.commit()

            # Enregistrer l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details)
            VALUES (%s, %s, %s, %s)
            """
            action_details = f"Match de tournoi ajouté entre {club_id} et les adversaires {', '.join(map(str, opponent_club_ids))} avec le score {score} (Tournoi: {tournament_id})"
            cursor.execute(
                history_query,
                ("tournament_match", tournament_id, "ajout", action_details)
            )
            conn.commit()

            # Récupérer l'ID de l'historique
            history_id = cursor.lastrowid

            # Mettre à jour la table tournaments avec l'ID de l'historique
            update_query = """
            UPDATE tournaments
            SET history_id = %s
            WHERE tournament_id = %s
            """
            cursor.execute(update_query, (history_id, tournament_id))
            conn.commit()

            await ctx.send("Match de tournoi ajouté avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout du match de tournoi : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")