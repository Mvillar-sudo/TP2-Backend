import mysql.connector
from mysql.connector import Error
import os

def get_db_connection():
    """
    Establece la conexión a la base de datos MySQL 
    usando variables de entorno o valores por defecto.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "mundial_db"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "eYFD050915_")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
