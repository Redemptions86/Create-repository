import aiomysql
from database.mysql_connection import connect_to_db  # Assurez-vous que cette fonction est asynchrone

# Ajouter un membre
async def add_member(discord_id, pseudo, club_id, force_team1, force_team2):
    query = """
    INSERT INTO members (discord_id, pseudo, club_id, force_team1, force_team2, creation_date)
    VALUES (%s, %s, %s, %s, %s, NOW())
    """
    conn = await connect_to_db()  # Connexion asynchrone
    if conn:
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (discord_id, pseudo, club_id, force_team1, force_team2)
                )
                await conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout du membre : {e}")
        finally:
            conn.close()

# Vérifier si un membre existe
async def member_exists(discord_id):
    query = "SELECT COUNT(*) FROM members WHERE discord_id = %s"
    conn = await connect_to_db()  # Connexion asynchrone
    if conn:
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (discord_id,))
                result = await cursor.fetchone()
                return result[0] > 0  # Renvoie True si le membre existe, sinon False
        except Exception as e:
            print(f"Erreur lors de la vérification de l'existence du membre : {e}")
        finally:
            conn.close()
    return False

# Récupérer un membre
async def get_member(discord_id):
    query = "SELECT * FROM members WHERE discord_id = %s"
    conn = await connect_to_db()  # Connexion asynchrone
    if conn:
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (discord_id,))
                result = await cursor.fetchone()
                return result
        except Exception as e:
            print(f"Erreur lors de la récupération du membre : {e}")
        finally:
            conn.close()

# Mettre à jour un membre
async def update_member(
        discord_id,
        pseudo=None,
        club_id=None,
        force_team1=None,
        force_team2=None):
    query = "UPDATE members SET "
    updates = []
    params = []

    if pseudo:
        updates.append("pseudo = %s")
        params.append(pseudo)
    if club_id:
        updates.append("club_id = %s")
        params.append(club_id)
    if force_team1:
        updates.append("force_team1 = %s")
        params.append(force_team1)
    if force_team2:
        updates.append("force_team2 = %s")
        params.append(force_team2)

    query += ", ".join(updates) + " WHERE discord_id = %s"
    params.append(discord_id)

    conn = await connect_to_db()  # Connexion asynchrone
    if conn:
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, tuple(params))
                await conn.commit()
        except Exception as e:
            print(f"Erreur lors de la mise à jour du membre : {e}")
        finally:
            conn.close()

# Supprimer un membre
async def delete_member(discord_id):
    query = "DELETE FROM members WHERE discord_id = %s"
    conn = await connect_to_db()  # Connexion asynchrone
    if conn:
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (discord_id,))
                await conn.commit()
        except Exception as e:
            print(f"Erreur lors de la suppression du membre : {e}")
        finally:
            conn.close()
