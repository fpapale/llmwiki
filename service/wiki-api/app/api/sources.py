from fastapi import APIRouter, HTTPException
from ..models.requests import ImportSourceRequest
from ..models.responses import ImportSourceResponse
from ..dependencies import get_file_service, get_path_service
import os

router = APIRouter(prefix="/sources", tags=["sources"])

@router.post("/import", response_model=ImportSourceResponse)
def import_source(req: ImportSourceRequest):
    file_service = get_file_service()
    path_service = get_path_service()
    
    file_path = path_service.get_raw_path(req.filename)
    
    if not path_service.is_safe_path(path_service.config.raw_dir, file_path):
        raise HTTPException(status_code=400, detail="Invalid path")
        
    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail="File already exists")
        
    file_service.write_file(file_path, req.content)
    
    return {"path": file_path}
