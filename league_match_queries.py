from database.mysql_connection import connect_to_db


def add_league_match(
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
        start_date,
        end_date,
        score,
        round):
    query = """
    INSERT INTO league_match (club_id, club_position, opponent_club_id_1, opponent_club_id_2, opponent_club_id_3, opponent_club_id_4, opponent_force_1, opponent_force_2, opponent_force_3, opponent_force_4, position_1, position_2, position_3, position_4, start_date, end_date, score, round)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
             start_date,
             end_date,
             score,
             round))
        conn.commit()
        cursor.close()
        conn.close()


def get_league_matches_in_progress():
    query = "SELECT * FROM league_match WHERE end_date IS NULL"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()  # Utiliser fetchall() pour récupérer plusieurs résultats
        cursor.close()
        conn.close()
        return result
    return None


def get_league_match(match_id):
    query = "SELECT * FROM league_match WHERE match_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (match_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result


def update_league_match(match_id, **kwargs):
    set_clause = ", ".join([f"{key} = %s" for key in kwargs])
    query = f"UPDATE league_match SET {set_clause} WHERE match_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (*kwargs.values(), match_id))
        conn.commit()
        cursor.close()
        conn.close()


def delete_league_match(match_id):
    query = "DELETE FROM league_match WHERE match_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (match_id,))
        conn.commit()
        cursor.close()
        conn.close()