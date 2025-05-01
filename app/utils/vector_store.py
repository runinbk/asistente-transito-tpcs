import os
import faiss
import numpy as np
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Cargar variables de entorno
load_dotenv()

# Singleton para mantener una única instancia del vector store
_vector_store_instance = None

# Ruta para guardar el índice FAISS
FAISS_INDEX_PATH = "faiss_index"

def get_or_create_vector_store():
    """
    Obtiene o crea una instancia singleton del vector store.
    """
    global _vector_store_instance
    
    if _vector_store_instance is None:
        # Crear embeddings con OpenAI
        embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Crear directorio para el índice si no existe
        os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
        
        # Verificar si existe un índice persistente
        if os.path.exists(FAISS_INDEX_PATH) and any(os.listdir(FAISS_INDEX_PATH)):
            try:
                _vector_store_instance = FAISS.load_local(
                    FAISS_INDEX_PATH,
                    embeddings
                )
                print("Vector store cargado desde disco.")
            except Exception as e:
                print(f"Error al cargar vector store: {e}")
                _vector_store_instance = FAISS.from_documents(
                    documents=[],
                    embedding=embeddings
                )
        else:
            # Crear un vector store vacío
            _vector_store_instance = FAISS.from_documents(
                documents=[Document(page_content="Inicialización del vector store", metadata={})],
                embedding=embeddings
            )
            # Guardar el índice inicial
            _vector_store_instance.save_local(FAISS_INDEX_PATH)
            
    return _vector_store_instance

def add_documents(texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None):
    """
    Añade documentos al vector store.
    
    Args:
        texts: Lista de textos a añadir
        metadatas: Metadatos asociados a cada texto
    """
    # Verificar que hay textos para añadir
    if not texts or len(texts) == 0:
        return 0
        
    # Obtener el vector store
    vector_store = get_or_create_vector_store()
    
    # Dividir textos en chunks para mejor procesamiento
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    # Preparar documentos
    documents = []
    for i, text in enumerate(texts):
        # Omitir textos vacíos
        if not text or text.strip() == "":
            continue
            
        chunks = text_splitter.split_text(text)
        for j, chunk in enumerate(chunks):
            metadata = {}
            if metadatas and i < len(metadatas):
                metadata = metadatas[i].copy()
            
            metadata["chunk"] = j
            
            documents.append(Document(
                page_content=chunk,
                metadata=metadata
            ))
    
    # Añadir documentos
    if documents:
        vector_store.add_documents(documents)
        
        # Guardar el índice actualizado
        vector_store.save_local(FAISS_INDEX_PATH)
    
    return len(documents)

def search(query: str, top_k: int = 3):
    """
    Busca documentos similares a la consulta.
    
    Args:
        query: Consulta a buscar
        top_k: Número de resultados a devolver
        
    Returns:
        Lista de documentos similares con sus puntuaciones
    """
    vector_store = get_or_create_vector_store()
    
    try:
        results = vector_store.similarity_search_with_score(query, k=top_k)
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)  # Convertir a float para asegurar serialización JSON
            }
            for doc, score in results
        ]
    except Exception as e:
        import logging
        logging.error(f"Error en la búsqueda vectorial: {str(e)}")
        return []