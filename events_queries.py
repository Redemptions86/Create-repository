from .mysql_connection import connect_to_db

def add_event(club_id, discord_id, total_points, start_date, end_date):
    """
    Ajoute un événement à la table events.
    """
    query = """
        INSERT INTO events (club_id, discord_id, total_points, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
    """
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, (club_id, discord_id, total_points, start_date, end_date))
            conn.commit()
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de l'événement : {e}")
        finally:
            cursor.close()
            conn.close()


def get_event(event_id):
    """
    Récupère un événement de la table events à partir de son ID.
    """
    query = "SELECT * FROM events WHERE event_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor(dictionary=True)  # Utilisation de dictionary=True pour un résultat clé/valeur
        try:
            cursor.execute(query, (event_id,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de l'événement : {e}")
            return None
        finally:
            cursor.close()
            conn.close()


def update_event(event_id, total_points=None, end_date=None):
    """
    Met à jour les informations d'un événement existant.
    """
    updates = []
    params = []

    if total_points is not None:
        updates.append("total_points = %s")
        params.append(total_points)

    if end_date is not None:
        updates.append("end_date = %s")
        params.append(end_date)

    if not updates:
        print("⚠️ Aucune donnée à mettre à jour.")
        return

    query = f"UPDATE events SET {', '.join(updates)} WHERE event_id = %s"
    params.append(event_id)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, tuple(params))
            conn.commit()
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour de l'événement : {e}")
        finally:
            cursor.close()
            conn.close()


def delete_event(event_id):
    """
    Supprime un événement de la table events.
    """
    query = "DELETE FROM events WHERE event_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, (event_id,))
            conn.commit()
        except Exception as e:
            print(f"❌ Erreur lors de la suppression de l'événement : {e}")
        finally:
            cursor.close()
            conn.close()
