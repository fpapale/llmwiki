import os
from .file_service import FileService
from .index_service import IndexService
from .path_service import PathService

class LintService:
    def __init__(self, file_service: FileService, index_service: IndexService, path_service: PathService):
        self.file_service = file_service
        self.index_service = index_service
        self.path_service = path_service

    def run_lint(self) -> dict:
        issues = []
        
        # Check core files
        core_files = [
            self.path_service.config.index_file,
            self.path_service.config.log_file,
            self.path_service.config.agent_file
        ]
        
        for cf in core_files:
            if not os.path.exists(cf):
                issues.append(f"Missing core file: {os.path.basename(cf)}")
                
        # Check for unindexed pages
        wiki_dir = self.path_service.config.wiki_dir
        wiki_files = self.file_service.list_files(wiki_dir, extension=".md")
        index_content = self.index_service.get_index()
        
        unindexed = []
        for wf in wiki_files:
            basename = os.path.basename(wf)
            if basename not in ["index.md", "log.md", "AGENT.MD"]:
                if basename not in index_content:
                    unindexed.append(basename)
                    issues.append(f"Unindexed page: {basename}")
                    
        return {
            "status": "issues_found" if issues else "ok",
            "issues": issues,
            "report": {
                "unindexed_pages": unindexed,
                "total_wiki_pages": len(wiki_files)
            }
        }
