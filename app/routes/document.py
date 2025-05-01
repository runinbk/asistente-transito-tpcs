from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
from typing import List
from app.services import chat_retrieval_service

router = APIRouter()

# Asegurarse de que el directorio para documentos existe
os.makedirs("documents", exist_ok=True)

@router.post("/documents/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Carga uno o más documentos y los guarda en el vector store."""
    try:
        # Guardar los archivos subidos en disco temporalmente
        file_paths = []
        for file in files:
            # Crear la ruta absoluta para el archivo
            file_location = os.path.abspath(f"documents/{file.filename}")
            
            # Guardar el archivo
            with open(file_location, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Almacenar la ruta del archivo
            file_paths.append(file_location)

        # Verificar que hay archivos para procesar
        if not file_paths:
            raise HTTPException(status_code=400, detail="No se proporcionaron archivos válidos")
            
        # Cargar documentos al vector store
        num_docs = chat_retrieval_service.load_and_store_documents(file_paths)
        
        return {
            "message": f"Documentos cargados exitosamente: {num_docs} fragmentos procesados",
            "files": [os.path.basename(path) for path in file_paths]
        }
    
    except Exception as e:
        # Proporcionar un mensaje de error más detallado para ayudar a depurar
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

@router.post("/documents/query")
async def query_documents(query: str = Form(...), top_k: int = Form(3)):
    """Consulta documentos relevantes según una pregunta."""
    try:
        results = chat_retrieval_service.query_documents(query, top_k=top_k)
        return {"results": results}
    
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)