from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def chat_endpoint(user_input: str):
    return {"response": f"Recibido tu mensaje: {user_input}"}
