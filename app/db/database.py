from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar las variables del .env
load_dotenv()

# Variables de entorno para la conexión
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")  # Valor por defecto
DB_PORT = os.getenv("POSTGRES_PORT", "5432")       # Valor por defecto

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de la base de datos con opciones para mejor depuración
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Para debug, establece en False en producción
    pool_pre_ping=True  # Verifica la conexión antes de usarla
)

# Crear una clase base para los modelos
Base = declarative_base()

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()