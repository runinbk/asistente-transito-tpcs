from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from app.utils.vector_store import get_or_create_vector_store
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AssistantAgent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Inicializar el modelo LLM (OpenAI)
        self.llm = ChatOpenAI(
            temperature=0.2,
            model_name="gpt-3.5-turbo",  # Puedes usar "gpt-4" para mejor calidad
            api_key=OPENAI_API_KEY
        )
        
        # Obtener el vector store
        self.vector_store = get_or_create_vector_store()
        
        # Inicializar la cadena de conversación
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )
    
    def process_message(self, query: str):
        """
        Procesa un mensaje del usuario y devuelve la respuesta del asistente.
        
        Args:
            query: Mensaje del usuario
            
        Returns:
            Respuesta del asistente y documentos fuente
        """
        try:
            # Aplicar pre-procesamiento (ej. diccionario de sinónimos)
            processed_query = self._preprocess_query(query)
            
            # Ejecutar la cadena de conversación
            result = self.chain({"question": processed_query})
            
            return {
                "answer": result["answer"],
                "source_documents": [doc.page_content for doc in result.get("source_documents", [])]
            }
        except Exception as e:
            return {
                "answer": f"Lo siento, ocurrió un error: {str(e)}",
                "source_documents": []
            }
    
    def _preprocess_query(self, query: str) -> str:
        """
        Preprocesa la consulta del usuario para mejorar la búsqueda.
        Por ejemplo, reemplaza términos comunes por sinónimos técnicos.
        
        Args:
            query: Consulta original
            
        Returns:
            Consulta procesada
        """
        # Diccionario simple de sinónimos (puedes expandirlo)
        sinonimos = {
            "multa": "sanción",
            "licencia": "permiso de conducir",
            "carnet": "permiso de conducir",
            "auto": "vehículo",
            "carro": "vehículo",
            "coche": "vehículo"
        }
        
        processed_query = query
        for palabra, sinonimo in sinonimos.items():
            processed_query = processed_query.replace(palabra, sinonimo)
            
        return processed_query