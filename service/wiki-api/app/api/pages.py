from fastapi import APIRouter, HTTPException
from ..models.responses import PageResponse
from ..dependencies import get_file_service, get_path_service
import os

router = APIRouter(prefix="/pages", tags=["pages"])

@router.get("/{slug}", response_model=PageResponse)
def get_page(slug: str):
    file_service = get_file_service()
    path_service = get_path_service()
    
    file_path = path_service.get_wiki_path(slug)
    
    # Ensure it's inside wiki dir
    if not path_service.is_safe_path(path_service.config.wiki_dir, file_path):
        raise HTTPException(status_code=400, detail="Invalid path")
        
    try:
        content = file_service.read_file(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")
        
    return {
        "title": slug.replace('-', ' ').title(),
        "slug": slug,
        "path": file_path,
        "content": content
    }
