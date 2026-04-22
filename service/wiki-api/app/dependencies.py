from .services.file_service import FileService
from .services.path_service import PathService
from .services.log_service import LogService
from .services.index_service import IndexService
from .services.llm_service import LLMService
from .services.ingest_service import IngestService
from .services.query_service import QueryService
from .services.lint_service import LintService
from .config import settings

path_service = PathService(settings.paths)
file_service = FileService(path_service)
log_service = LogService(file_service, settings.paths.log_file)
index_service = IndexService(file_service, settings.paths.index_file)
llm_service = LLMService(settings.llm, settings.features)
ingest_service = IngestService(file_service, log_service, index_service, llm_service)
query_service = QueryService(file_service, index_service, log_service, llm_service)
lint_service = LintService(file_service, index_service, path_service)

def get_file_service():
    return file_service

def get_ingest_service():
    return ingest_service

def get_query_service():
    return query_service

def get_lint_service():
    return lint_service

def get_path_service():
    return path_service
