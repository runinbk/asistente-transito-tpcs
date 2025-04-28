from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    def __init__(self):
        self.documents: List[str] = []
        self.vectorizer = TfidfVectorizer()
        self.vectors = None

    def add_documents(self, docs: List[str]):
        """Agrega nuevos documentos al almacenamiento."""
        self.documents.extend(docs)
        self.vectors = self.vectorizer.fit_transform(self.documents)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Busca los documentos más similares al query."""
        if not self.vectors:
            raise ValueError("No hay documentos cargados.")

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.vectors).flatten()

        # Obtener los índices de los documentos más similares
        top_indices = similarities.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append((self.documents[idx], similarities[idx]))

        return results