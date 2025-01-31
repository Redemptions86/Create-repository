import aiomysql
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Variables de connexion
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))  # Récupération du port depuis le fichier .env
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "botxcrew")

# Fonction pour obtenir une connexion à la base de données
async def connect_to_db():
    """Créer une connexion à la base de données."""
    try:
        connection = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,  # Ajout du port dans la connexion
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            autocommit=True  # Pour éviter d'appeler commit manuellement
        )
        print("Connexion à la base de données réussie.")
        return connection
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

# Fonction pour exécuter une requête SQL
async def execute_query(query, params=None):
    """Exécuter une requête SQL de manière asynchrone."""
    connection = await connect_to_db()
    if connection is None:
        print("Impossible de se connecter à la base de données.")
        return None
    try:
        async with connection.cursor() as cursor:  # Enlever dictionary=True
            await cursor.execute(query, params)
            if query.strip().lower().startswith('select'):
                result = await cursor.fetchall()
            else:
                result = None
            return result
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")
        return None
    finally:
        connection.close()  # Fermer la connexion après l'exécution de la requête