from app.db.database import Base, engine
from app.models.chat_session import ChatSession  # Asegúrate de importar tus modelos

print("Creando las tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("¡Tablas creadas exitosamente!")
