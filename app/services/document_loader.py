import os
import PyPDF2
import fitz  # PyMuPDF
from typing import List, Dict, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def load_text_file(file_path: str) -> tuple:
    """
    Carga un archivo de texto plano.
    
    Returns:
        (contenido, metadata)
    """
    full_path = os.path.join(BASE_DIR, file_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = {
        "source": file_path,
        "type": "text",
        "filename": os.path.basename(file_path)
    }
    
    return content, metadata

def load_pdf_file(file_path: str) -> tuple:
    """
    Carga un archivo PDF y extrae su texto.
    
    Returns:
        (contenido, metadata)
    """
    full_path = os.path.join(BASE_DIR, file_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    try:
        # Intenta primero con PyMuPDF (más robusto)
        doc = fitz.open(full_path)
        content = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            content += page.get_text()
        doc.close()
    except Exception as e:
        # Fallback a PyPDF2
        try:
            with open(full_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                content = ""
                for page_num in range(len(pdf_reader.pages)):
                    content += pdf_reader.pages[page_num].extract_text()
        except Exception as e2:
            raise ValueError(f"No se pudo leer el PDF: {str(e)} / {str(e2)}")
    
    metadata = {
        "source": file_path,
        "type": "pdf",
        "filename": os.path.basename(file_path)
    }
    
    return content, metadata

def load_documents(file_paths: List[str]) -> tuple:
    """
    Carga múltiples documentos de diferentes tipos.
    
    Returns:
        (contenidos, metadatos)
    """
    contents = []
    metadatas = []
    
    for path in file_paths:
        if path.lower().endswith(".txt"):
            content, metadata = load_text_file(path)
            contents.append(content)
            metadatas.append(metadata)
        elif path.lower().endswith(".pdf"):
            content, metadata = load_pdf_file(path)
            contents.append(content)
            metadatas.append(metadata)
        else:
            raise ValueError(f"Tipo de archivo no soportado: {path}")
    
    return contents, metadatas