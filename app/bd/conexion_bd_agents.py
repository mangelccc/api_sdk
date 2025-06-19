import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    print("conexion exitosa")
except Exception as ex:
    print(ex)