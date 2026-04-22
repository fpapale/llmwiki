import os
from .file_service import FileService
from .log_service import LogService
from .index_service import IndexService
from .llm_service import LLMService

class IngestService:
    def __init__(self, file_service: FileService, log_service: LogService, index_service: IndexService, llm_service: LLMService):
        self.file_service = file_service
        self.log_service = log_service
        self.index_service = index_service
        self.llm_service = llm_service

    def run_ingest(self, source_path: str, mode: str) -> list[str]:
        # Resolve source absolute path based on workspace (simulated via path_service inside file_service)
        # For MVP, assuming source_path is relative to workspace or absolute.
        # Let's assume it's passed as is and we can read it.
        # We need the abs path to raw/ file. 
        abs_source_path = os.path.abspath(os.path.join(self.file_service.path_service.config.vault_root, source_path))
        
        content = self.file_service.read_file(abs_source_path)
        
        # generate summary
        summary = self.llm_service.generate_summary(content)
        
        # save summary to wiki/
        filename = os.path.basename(source_path)
        summary_filename = f"{os.path.splitext(filename)[0]}-summary.md"
        summary_path = self.file_service.path_service.get_wiki_path(summary_filename)
        
        self.file_service.write_file(summary_path, summary)
        
        # update index
        self.index_service.add_entry(f"- [{summary_filename}]({summary_filename}): Summary of {filename}")
        
        # log operation
        self.log_service.add_entry(
            operation="ingest",
            title=filename,
            details=[f"created: wiki/{summary_filename}", "updated: wiki/index.md", "updated: wiki/log.md"]
        )
        
        return [summary_path, self.index_service.index_file_path, self.log_service.log_file_path]
