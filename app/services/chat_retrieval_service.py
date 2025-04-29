from app.services.document_loader import load_documents
from app.utils.vector_store import add_documents, search

def load_and_store_documents(file_paths: list):
    """
    Carga documentos desde archivos y los almacena en el vector store.
    
    Args:
        file_paths: Lista de rutas a los archivos
        
    Returns:
        Número de documentos cargados
    """
    contents, metadatas = load_documents(file_paths)
    return add_documents(contents, metadatas)

def query_documents(query: str, top_k: int = 3):
    """
    Realiza una búsqueda en los documentos almacenados.
    
    Args:
        query: Consulta a buscar
        top_k: Número de resultados a devolver
        
    Returns:
        Lista de documentos similares con sus puntuaciones
    """
    return search(query, top_k=top_k)