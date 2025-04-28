import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.vector_store import VectorStore

if __name__ == "__main__":
    store = VectorStore()
    store.add_documents([
        "El perro corre en el parque.",
        "La computadora procesa información.",
        "El gato duerme en el sofá."
    ])

    results = store.search("animal descansando", top_k=2)

    for doc, score in results:
        print(f"Score: {score:.2f} - Documento: {doc}")