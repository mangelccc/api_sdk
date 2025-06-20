import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Crea y retorna una nueva conexión a la base de datos
    """
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Exception as ex:
        print(f"Error conectando a la base de datos: {ex}")
        raise ex

# Test de conexión (opcional - solo se ejecuta si corres este archivo directamente)
if __name__ == "__main__":
    try:
        conn = get_db_connection()
        print("Conexión exitosa")
        conn.close()
    except Exception as ex:
        print(f"Error en test de conexión: {ex}")