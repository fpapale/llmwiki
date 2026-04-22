from fastapi import APIRouter, HTTPException
from ..models.requests import QueryRequest
from ..models.responses import QueryResponse
from ..dependencies import get_query_service

router = APIRouter(prefix="/query", tags=["query"])

@router.post("/run", response_model=QueryResponse)
def run_query(req: QueryRequest):
    query_service = get_query_service()
    try:
        answer, sources = query_service.run_query(req.question)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
