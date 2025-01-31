import aiomysql
from database.mysql_connection import connect_to_db  # Si vous avez une fonction connect_to_db asynchrone

# Assurez-vous que connect_to_db() est asynchrone

async def add_command(command_name, description):
    query = "INSERT INTO commands (command_name, description) VALUES (%s, %s)"
    conn = await connect_to_db()  # Utilisation de la version asynchrone de la connexion
    if conn:
        async with conn.cursor() as cursor:  # Utilisation du curseur de manière asynchrone
            await cursor.execute(query, (command_name, description))
            await conn.commit()

async def get_command(command_id):
    query = "SELECT * FROM commands WHERE command_id = %s"
    conn = await connect_to_db()  # Connexion asynchrone
    if conn:
        async with conn.cursor() as cursor:  # Utilisation du curseur de manière asynchrone
            await cursor.execute(query, (command_id,))
            result = await cursor.fetchone()
            return result

async def update_command(command_id, **kwargs):
    set_clause = ", ".join([f"{key} = %s" for key in kwargs])
    query = f"UPDATE commands SET {set_clause} WHERE command_id = %s"
    conn = await connect_to_db()  # Connexion asynchrone
    if conn:
        async with conn.cursor() as cursor:  # Utilisation du curseur de manière asynchrone
            await cursor.execute(query, (*kwargs.values(), command_id))
            await conn.commit()

async def delete_command(command_id):
    query = "DELETE FROM commands WHERE command_id = %s"
    conn = await connect_to_db()  # Connexion asynchrone
    if conn:
        async with conn.cursor() as cursor:  # Utilisation du curseur de manière asynchrone
            await cursor.execute(query, (command_id,))
            await conn.commit()