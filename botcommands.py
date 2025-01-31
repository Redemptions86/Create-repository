from database.mysql_connection import connect_to_db

async def create_tournament(
        club_id,
        club_position,
        opponent_club_ids,
        opponent_forces,
        positions,
        round,
        status,
        start_date,
        score):
    """Créer un tournoi dans la base de données de manière asynchrone."""
    conn = await connect_to_db()
    try:
        async with conn.cursor() as cursor:
            query = """
                INSERT INTO tournaments (club_id, club_position, opponent_club_ids, opponent_forces, positions, round, status, start_date, score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            await cursor.execute(
                query,
                (club_id,
                 club_position,
                 opponent_club_ids,
                 opponent_forces,
                 positions,
                 round,
                 status,
                 start_date,
                 score)
            )
            await conn.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la création du tournoi : {e}")
    finally:
        conn.close()

async def add_club_with_validation(club_name, club_owner):
    """Ajouter un club à la base de données avec validation de manière asynchrone."""
    if not club_name or not club_owner:
        return "Le nom du club et le propriétaire ne peuvent pas être vides."

    conn = await connect_to_db()
    try:
        async with conn.cursor() as cursor:
            # Vérifier si le club existe déjà
            await cursor.execute("SELECT * FROM clubs WHERE name = %s", (club_name,))
            existing_club = await cursor.fetchone()
            if existing_club:
                return f"Un club avec le nom '{club_name}' existe déjà."

            # Ajouter le club
            query = "INSERT INTO clubs (name, owner) VALUES (%s, %s)"
            await cursor.execute(query, (club_name, club_owner))
            await conn.commit()
            return "Le club a été ajouté avec succès."
    except Exception as e:
        raise Exception(f"Erreur lors de l'ajout du club : {e}")
    finally:
        conn.close()

async def get_club_by_name(club_name):
    """Récupérer un club par son nom de manière asynchrone."""
    conn = await connect_to_db()
    try:
        async with conn.cursor() as cursor:
            query = "SELECT * FROM clubs WHERE name = %s"
            await cursor.execute(query, (club_name,))
            club = await cursor.fetchone()
            return club
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération du club : {e}")
    finally:
        conn.close()


# Ajout de la fonction setup pour enregistrer ce fichier comme un cog
async def setup(bot):
    """Enregistrer ce cog dans le bot de manière asynchrone."""
    pass