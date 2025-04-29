import os
import faiss
import numpy as np
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Cargar variables de entorno
load_dotenv()

# Singleton para mantener una única instancia del vector store
_vector_store_instance = None

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
        
        # Verificar si existe un índice persistente
        if os.path.exists("faiss_index") and os.path.isdir("faiss_index"):
            try:
                _vector_store_instance = FAISS.load_local(
                    "faiss_index",
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
                documents=[],
                embedding=embeddings
            )
            
    return _vector_store_instance

def add_documents(texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None):
    """
    Añade documentos al vector store.
    
    Args:
        texts: Lista de textos a añadir
        metadatas: Metadatos asociados a cada texto
    """
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
        vector_store.save_local("faiss_index")
    
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
    results = vector_store.similarity_search_with_score(query, k=top_k)
    
    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": score
        }
        for doc, score in results
    ]