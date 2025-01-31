def add_force(member_id, force_value):
    query = "INSERT INTO forces (member_id, force_value) VALUES (%s, %s)"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (member_id, force_value))
        conn.commit()
        cursor.close()
        conn.close()


def get_force(member_id):
    query = "SELECT force_value FROM forces WHERE member_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (member_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
