from fastapi import APIRouter, HTTPException
from ..models.requests import IngestRequest
from ..models.responses import IngestResponse
from ..dependencies import get_ingest_service

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/run", response_model=IngestResponse)
def run_ingest(req: IngestRequest):
    ingest_service = get_ingest_service()
    try:
        touched = ingest_service.run_ingest(req.source_path, req.mode)
        return {"touched_files": touched}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
