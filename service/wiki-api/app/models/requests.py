from pydantic import BaseModel
from typing import Optional

class ImportSourceRequest(BaseModel):
    filename: str
    content: str

class IngestRequest(BaseModel):
    source_path: str
    mode: str = "summary_only"

class QueryRequest(BaseModel):
    question: str
