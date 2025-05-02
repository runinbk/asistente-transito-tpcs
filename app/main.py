from fastapi import FastAPI
from app.routes import chat, document, chat_message, message, agent_chat

from app.db.database import engine, Base

app = FastAPI(
    title="Asistente de Tránsito",
    description="API para gestionar sesiones y mensajes de chat del asistente de tránsito",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# Registrar routers
app.include_router(chat.router, prefix="/api", tags=["Chat Sessions"])
app.include_router(chat_message.router, prefix="/api", tags=["Chat Messages"])
app.include_router(document.router, prefix="/api")
app.include_router(message.router)  # Este router ahora tiene la lógica del agente integrada
app.include_router(agent_chat.router)  # Mantenemos este router por compatibilidad

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido al asistente de tránsito!"}