from fastapi import FastAPI
from app.routes import chat, document
from app.routes.chat import router as ChatRouter

app = FastAPI(
    title="Agente de Normativa de Tránsito",
    version="0.1.0"
)

# Registrar routers
app.include_router(chat.router, prefix="/api")
app.include_router(document.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente 🚀"}
