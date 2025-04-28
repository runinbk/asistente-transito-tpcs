
import os
from typing import List

def load_text_file(file_path: str) -> str:
    """Carga un archivo de texto plano (.txt)"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content

def load_pdf_file(file_path: str) -> str:
    """Carga un archivo PDF y extrae su texto"""
    from PyPDF2 import PdfReader

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def load_documents(file_paths: List[str]) -> List[str]:
    """Carga una lista de archivos y devuelve una lista de contenidos de texto"""
    contents = []
    for path in file_paths:
        if path.lower().endswith(".txt"):
            contents.append(load_text_file(path))
        elif path.lower().endswith(".pdf"):
            contents.append(load_pdf_file(path))
        else:
            raise ValueError(f"Formato de archivo no soportado: {path}")
    return contents