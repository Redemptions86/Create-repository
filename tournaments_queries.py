from database.mysql_connection import connect_to_db


def add_tournament(
        club_id,
        club_position,
        opponent_club_id_1,
        opponent_club_id_2,
        opponent_club_id_3,
        opponent_club_id_4,
        opponent_force_1,
        opponent_force_2,
        opponent_force_3,
        opponent_force_4,
        position_1,
        position_2,
        position_3,
        position_4,
        round,
        status,
        start_date,
        end_date,
        score):
    query = """
    INSERT INTO tournaments (club_id, club_position, opponent_club_id_1, opponent_club_id_2, opponent_club_id_3, opponent_club_id_4, opponent_force_1, opponent_force_2, opponent_force_3, opponent_force_4, position_1, position_2, position_3, position_4, round, status, start_date, end_date, score)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            query,
            (club_id,
             club_position,
             opponent_club_id_1,
             opponent_club_id_2,
             opponent_club_id_3,
             opponent_club_id_4,
             opponent_force_1,
             opponent_force_2,
             opponent_force_3,
             opponent_force_4,
             position_1,
             position_2,
             position_3,
             position_4,
             round,
             status,
             start_date,
             end_date,
             score))
        conn.commit()
        cursor.close()  # Fermeture de la connexion
        cursor.close()
        conn.close()


def get_tournaments_in_progress():
    query = "SELECT * FROM tournaments WHERE end_date IS NULL"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()  # Utiliser fetchall() pour récupérer plusieurs résultats
        cursor.close()
        conn.close()
        return result
    return None


def get_tournament_by_id(tournament_id):
    query = "SELECT * FROM tournaments WHERE tournament_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (tournament_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    return None


def update_tournament_score(tournament_id, score):
    query = "UPDATE tournaments SET score = %s WHERE tournament_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (score, tournament_id))
        conn.commit()
        cursor.close()
        conn.close()