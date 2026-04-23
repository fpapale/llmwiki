from .file_service import FileService
from .index_service import IndexService
from .log_service import LogService
from .llm_service import LLMService

class QueryService:
    def __init__(self, file_service: FileService, index_service: IndexService, log_service: LogService, llm_service: LLMService):
        self.file_service = file_service
        self.index_service = index_service
        self.log_service = log_service
        self.llm_service = llm_service

    def run_query(self, question: str) -> tuple[str, list[str]]:
        # Read index and log for context
        index_content = self.index_service.get_index()
        
        # Se ci sono righe di fonti aggiunte (es. '- ['), rimuoviamo il placeholder per non confondere l'LLM
        if "*Nessuna fonte indicizzata al momento.*" in index_content and "- [" in index_content:
            index_content = index_content.replace("*Nessuna fonte indicizzata al momento.*", "")
            
        log_content = self.log_service.get_logs()
        
        context = f"INDEX:\n{index_content}\n\nLOG:\n{log_content}"
        
        answer = self.llm_service.answer_query(question, context)
        
        sources = ["wiki/index.md", "wiki/log.md"]
        return answer, sources
