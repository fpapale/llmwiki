from pydantic import BaseModel
from typing import List, Dict, Any

class HealthResponse(BaseModel):
    status: str
    service: str

class ConfigResponse(BaseModel):
    paths: Dict[str, str]
    llm_provider: str
    llm_model: str

class PageResponse(BaseModel):
    title: str
    slug: str
    path: str
    content: str

class ImportSourceResponse(BaseModel):
    path: str

class IngestResponse(BaseModel):
    touched_files: List[str]

class QueryResponse(BaseModel):
    answer: str
    sources: List[str] = []

class LintResponse(BaseModel):
    status: str
    issues: List[str]
    report: Dict[str, Any]
