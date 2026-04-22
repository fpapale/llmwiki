from fastapi import FastAPI
from .api import health, pages, sources, ingest, query, lint
from .config import settings
import logging

# Configure logging
logging.basicConfig(level=settings.app.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app.name)

# Include routers
app.include_router(health.router)
app.include_router(pages.router)
app.include_router(sources.router)
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(lint.router)

@app.get("/config")
def get_config():
    """
    Restituisce una versione sicura della configurazione
    """
    return {
        "paths": {
            "vault_root": settings.paths.vault_root,
            "raw_dir": settings.paths.raw_dir,
            "wiki_dir": settings.paths.wiki_dir
        },
        "llm_provider": settings.llm.provider,
        "llm_model": settings.llm.model
    }
