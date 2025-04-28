from fastapi import FastAPI
from app.routes import chat
from app.routes.chat import router as ChatRouter

app = FastAPI(
    title="Agente de Normativa de Tránsito",
    version="0.1.0"
)

# rutas
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente 🚀"}
