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

@router.get("/unprocessed")
def get_unprocessed_sources():
    file_service = get_file_service()
    path_service = get_path_service()
    
    raw_files = file_service.list_files(path_service.config.raw_dir)
    valid_exts = [".md", ".pdf", ".docx", ".xlsx"]
    raw_files = [f for f in raw_files if os.path.splitext(f)[1].lower() in valid_exts]
    
    wiki_files = file_service.list_files(path_service.config.wiki_dir, extension="-summary.md")
    
    # Extract basenames without '-summary.md'
    processed_basenames = [os.path.basename(wf).replace("-summary.md", "") for wf in wiki_files]
    
    unprocessed = []
    for rf in raw_files:
        basename = os.path.splitext(os.path.basename(rf))[0]
        if basename not in processed_basenames:
            # Return relative path e.g. "raw/filename.md"
            rel_path = os.path.relpath(rf, path_service.config.vault_root)
            # Ensure forward slashes
            unprocessed.append(rel_path.replace("\\", "/"))
            
    return {"unprocessed": unprocessed}
