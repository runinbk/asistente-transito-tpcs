from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from app.services import chat_retrieval_service

router = APIRouter()

@router.post("/documents/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Carga uno o más documentos y los guarda en el vector store."""
    try:
        # Guardar los archivos subidos en disco temporalmente
        file_paths = []
        for file in files:
            file_location = f"documents/{file.filename}"
            with open(file_location, "wb") as f:
                content = await file.read()
                f.write(content)
            file_paths.append(file_location)

        # Cargar documentos al vector store
        chat_retrieval_service.load_and_store_documents(file_paths)
        
        return {"message": "Documentos cargados exitosamente"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/query")
async def query_documents(query: str = Form(...), top_k: int = Form(3)):
    """Consulta documentos relevantes según una pregunta."""
    try:
        results = chat_retrieval_service.query_documents(query, top_k=top_k)
        return {"results": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
