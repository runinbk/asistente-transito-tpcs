import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def load_text_file(file_path: str) -> str:
    """Carga un archivo de texto plano."""
    full_path = os.path.join(BASE_DIR, file_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_documents(file_paths: list) -> list:
    """Carga múltiples documentos de diferentes tipos."""
    contents = []
    for path in file_paths:
        if path.endswith(".txt"):
            contents.append(load_text_file(path))
        else:
            raise ValueError(f"Tipo de archivo no soportado: {path}")
    return contents