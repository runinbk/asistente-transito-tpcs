from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Variables de entorno para la conexión
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def run_migration():
    """
    Actualiza los campos created_at NULL existentes a la fecha actual
    """
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Actualizar created_at en chat_sessions donde sea NULL
        connection.execute(text(
            "UPDATE chat_sessions SET created_at = NOW() WHERE created_at IS NULL"
        ))
        
        # Actualizar created_at en chat_messages donde sea NULL
        connection.execute(text(
            "UPDATE chat_messages SET created_at = NOW() WHERE created_at IS NULL"
        ))
        
        # Hacer created_at NOT NULL en ambas tablas
        connection.execute(text(
            "ALTER TABLE chat_sessions ALTER COLUMN created_at SET NOT NULL"
        ))
        
        connection.execute(text(
            "ALTER TABLE chat_messages ALTER COLUMN created_at SET NOT NULL"
        ))
        
        connection.commit()
    
    print("Migración completada: campos created_at actualizados y establecidos como NOT NULL")

if __name__ == "__main__":
    run_migration()