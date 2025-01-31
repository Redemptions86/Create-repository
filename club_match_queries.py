from database.mysql_connection import execute_query, connect_to_db

# Fonction pour ajouter un match de club
async def add_club_match(
        club_id,
        opponent_club_1,
        opponent_club_2,
        opponent_club_3,
        opponent_club_4,
        start_date,
        end_date):
    query = """
    INSERT INTO club_match (club_id, opponent_club_1, opponent_club_2, opponent_club_3, opponent_club_4, start_date, end_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (club_id, opponent_club_1, opponent_club_2, opponent_club_3, opponent_club_4, start_date, end_date)
    await execute_query(query, params)  # Utilisation de la fonction asynchrone pour exécuter la requête


# Fonction pour obtenir un match de club
async def get_club_match(match_id):
    query = "SELECT * FROM club_match WHERE match_id = %s"
    params = (match_id,)
    result = await execute_query(query, params)  # Utilisation de la fonction asynchrone pour exécuter la requête
    return result


# Fonction pour mettre à jour un match de club
async def update_club_match(match_id, **kwargs):
    query = "UPDATE club_match SET "
    updates = []
    params = []

    for key, value in kwargs.items():
        updates.append(f"{key} = %s")
        params.append(value)

    query += ", ".join(updates) + " WHERE match_id = %s"
    params.append(match_id)

    await execute_query(query, tuple(params))  # Utilisation de la fonction asynchrone pour exécuter la requête


# Fonction pour supprimer un match de club
async def delete_club_match(match_id):
    query = "DELETE FROM club_match WHERE match_id = %s"
    params = (match_id,)
    await execute_query(query, params)  # Utilisation de la fonction asynchrone pour exécuter la requête


# Fonction setup pour l'enregistrement du fichier comme un cog
async def setup(bot):
    """Enregistrer ce fichier comme un cog dans le bot."""
    pass