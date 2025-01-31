from database.mysql_connection import execute_query

# Fonction pour ajouter la force d'un club
async def add_club_force(club_id, total_force):
    query = "INSERT INTO club_forces (club_id, total_force) VALUES (%s, %s)"
    params = (club_id, total_force)
    await execute_query(query, params)

# Fonction pour obtenir la force d'un club
async def get_club_force(club_id):
    query = "SELECT total_force FROM club_forces WHERE club_id = %s"
    params = (club_id,)
    result = await execute_query(query, params)
    return result