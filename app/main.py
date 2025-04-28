from fastapi import FastAPI
from app.routes import chat, document, chat_message

app = FastAPI(
    title="Asistente de Tránsito",
    description="API para gestionar sesiones y mensajes de chat del asistente de tránsito",
    version="1.0.0"
)

# Registrar routers
app.include_router(chat.router, prefix="/api", tags=["Chat Sessions"])
app.include_router(chat_message.router, prefix="/api", tags=["Chat Messages"])
app.include_router(document.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido al asistente de tránsito!"}
