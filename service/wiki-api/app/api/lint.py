from fastapi import APIRouter, HTTPException
from ..models.responses import LintResponse
from ..dependencies import get_lint_service

router = APIRouter(prefix="/lint", tags=["lint"])

@router.post("/run", response_model=LintResponse)
def run_lint():
    lint_service = get_lint_service()
    try:
        res = lint_service.run_lint()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
