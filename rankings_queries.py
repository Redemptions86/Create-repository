from database.mysql_connection import connect_to_db


def add_ranking(
        club_id,
        club_name,
        total_forces,
        total_matches_played,
        total_wins,
        total_losses,
        total_points,
        ranking_position):
    query = """
    INSERT INTO rankings (club_id, club_name, total_forces, total_matches_played, total_wins, total_losses, total_points, ranking_position)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            query,
            (club_id,
             club_name,
             total_forces,
             total_matches_played,
             total_wins,
             total_losses,
             total_points,
             ranking_position))
        conn.commit()
        cursor.close()
        conn.close()


def get_ranking_by_club(club_id):
    query = "SELECT * FROM rankings WHERE club_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (club_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result


def update_ranking(club_id, **kwargs):
    query = "UPDATE rankings SET "
    updates = []
    params = []

    for key, value in kwargs.items():
        updates.append(f"{key} = %s")
        params.append(value)

    query += ", ".join(updates) + " WHERE club_id = %s"
    params.append(club_id)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        conn.commit()
        cursor.close()
        conn.close()


def delete_ranking(club_id):
    query = "DELETE FROM rankings WHERE club_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (club_id,))
        conn.commit()
        cursor.close()
        conn.close()
