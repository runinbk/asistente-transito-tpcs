from app.utils.vector_store import VectorStore
from app.services.document_loader import load_documents

# Instancia global de VectorStore (opcionalmente en el futuro puede mejorarse para persistir en base de datos o archivos)
vector_store = VectorStore()

def load_and_store_documents(file_paths: list):
    """Carga documentos desde archivos y los almacena en el vector store."""
    documents = load_documents(file_paths)
    vector_store.add_documents(documents)

def query_documents(query: str, top_k: int = 3):
    """Realiza una búsqueda en los documentos almacenados."""
    return vector_store.search(query, top_k=top_k)