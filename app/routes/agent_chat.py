from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chat_message import ChatMessageCreate, ChatMessageResponse
from app.services.agent import AssistantAgent
from app.db.database import get_db
from app.services import chat_message_service
from typing import Dict
import os

router = APIRouter(
    prefix="/api/agent",
    tags=["AI Assistant"]
)

# Caché de agentes por sesión
agents_cache: Dict[str, AssistantAgent] = {}

def get_agent_for_session(session_id: int):
    """
    Obtiene o crea un agente para una sesión específica.
    """
    session_key = str(session_id)
    
    if session_key not in agents_cache:
        agents_cache[session_key] = AssistantAgent(session_key)
        
    return agents_cache[session_key]

@router.post("/chat/{session_id}", response_model=ChatMessageResponse)
def chat_with_agent(
    session_id: int,
    message_data: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """
    Envía un mensaje al agente y guarda la conversación.
    """
    # Verificar que el session_id coincide
    if message_data.session_id != session_id:
        raise HTTPException(status_code=400, detail="El ID de sesión no coincide")
    
    # Verificar que el remitente es el usuario
    if message_data.sender != "user":
        raise HTTPException(status_code=400, detail="El remitente debe ser 'user'")
    
    try:
        # Guardar mensaje del usuario
        user_message = chat_message_service.create_chat_message(db, message_data)
        
        # Procesar con el agente
        agent = get_agent_for_session(session_id)
        response = agent.process_message(message_data.message)
        
        # Crear y guardar respuesta del asistente
        assistant_message_data = ChatMessageCreate(
            session_id=session_id,
            sender="assistant",
            message=response["answer"]
        )
        
        assistant_message = chat_message_service.create_chat_message(db, assistant_message_data)
        
        return assistant_message
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el mensaje: {str(e)}")