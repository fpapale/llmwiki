from datetime import datetime
from .file_service import FileService

class LogService:
    def __init__(self, file_service: FileService, log_file_path: str):
        self.file_service = file_service
        self.log_file_path = log_file_path

    def add_entry(self, operation: str, title: str, details: list[str]) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n## [{now}] {operation} | {title}\n"
        for detail in details:
            entry += f"- {detail}\n"
        self.file_service.append_file(self.log_file_path, entry)

    def get_logs(self) -> str:
        try:
            return self.file_service.read_file(self.log_file_path)
        except FileNotFoundError:
            return ""
