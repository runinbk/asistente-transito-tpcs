import os
import PyPDF2
import fitz  # PyMuPDF
from typing import List, Dict, Any, Tuple

def load_text_file(file_path: str) -> Tuple[str, Dict[str, str]]:
    """
    Carga un archivo de texto plano.
    
    Args:
        file_path: Ruta al archivo de texto
        
    Returns:
        Tupla (contenido, metadata)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Intentar con otra codificación si UTF-8 falla
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    metadata = {
        "source": file_path,
        "type": "text",
        "filename": os.path.basename(file_path)
    }
    
    return content, metadata

def load_pdf_file(file_path: str) -> Tuple[str, Dict[str, str]]:
    """
    Carga un archivo PDF y extrae su texto.
    
    Args:
        file_path: Ruta al archivo PDF
        
    Returns:
        Tupla (contenido, metadata)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    try:
        # Intenta primero con PyMuPDF (más robusto)
        doc = fitz.open(file_path)
        content = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            content += page.get_text()
        doc.close()
    except Exception as e:
        # Fallback a PyPDF2
        try:
            with open(file_path, 'rb') as f:
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

def load_documents(file_paths: List[str]) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    Carga múltiples documentos de diferentes tipos.
    
    Args:
        file_paths: Lista de rutas a los archivos
        
    Returns:
        Tupla (contenidos, metadatos)
    """
    contents = []
    metadatas = []
    
    for path in file_paths:
        try:
            if path.lower().endswith(".txt"):
                content, metadata = load_text_file(path)
                contents.append(content)
                metadatas.append(metadata)
            elif path.lower().endswith(".pdf"):
                content, metadata = load_pdf_file(path)
                contents.append(content)
                metadatas.append(metadata)
            else:
                print(f"Tipo de archivo no soportado: {path}")
                continue
        except Exception as e:
            print(f"Error al cargar el archivo {path}: {str(e)}")
            continue
    
    return contents, metadatas