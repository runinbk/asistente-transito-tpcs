from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.schemas.message import MessageCreate, MessageResponse
from app.services import message_service
from app.db.database import get_db
from typing import List
from app.services.agent import AssistantAgent

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

# Caché de agentes por sesión
agents_cache = {}

def get_agent_for_session(session_id: int):
    """
    Obtiene o crea un agente para una sesión específica.
    """
    session_key = str(session_id)
    
    if session_key not in agents_cache:
        agents_cache[session_key] = AssistantAgent(session_key)
        
    return agents_cache[session_key]

@router.post("/", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    # Primero guardamos el mensaje del usuario
    user_message = message_service.create_message(db, message)
    
    try:
        # Procesamos con el agente para obtener una respuesta
        agent = get_agent_for_session(message.session_id)
        response = agent.process_message(message.message)
        
        # Crear y guardar respuesta del asistente
        assistant_message_data = MessageCreate(
            session_id=message.session_id,
            sender="assistant",
            message=response["answer"]
        )
        
        # Guardamos el mensaje del asistente
        assistant_message = message_service.create_message(db, assistant_message_data)
        
        return assistant_message
        
    except Exception as e:
        # Si hay un error, registramos el error pero devolvemos el mensaje del usuario
        print(f"Error al procesar con el agente: {str(e)}")
        return user_message

@router.get("/session/{session_id}", response_model=List[MessageResponse])
def get_messages(session_id: int, db: Session = Depends(get_db)):
    return message_service.get_messages_by_session(db, session_id)

@router.post("/query/{session_id}", response_model=MessageResponse)
def query_agent(
    session_id: int, 
    query: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    Endpoint simplificado para enviar una consulta y recibir respuesta del agente
    """
    # Crear el mensaje del usuario
    message_data = MessageCreate(
        session_id=session_id,
        sender="user",
        message=query
    )
    
    # Guardar mensaje del usuario
    user_message = message_service.create_message(db, message_data)
    
    try:
        # Procesar con el agente
        agent = get_agent_for_session(session_id)
        response = agent.process_message(query)
        
        # Crear y guardar respuesta del asistente
        assistant_message_data = MessageCreate(
            session_id=session_id,
            sender="assistant",
            message=response["answer"]
        )
        
        assistant_message = message_service.create_message(db, assistant_message_data)
        
        return assistant_message
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el mensaje: {str(e)}")