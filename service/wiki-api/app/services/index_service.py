from .file_service import FileService

class IndexService:
    def __init__(self, file_service: FileService, index_file_path: str):
        self.file_service = file_service
        self.index_file_path = index_file_path

    def get_index(self) -> str:
        try:
            return self.file_service.read_file(self.index_file_path)
        except FileNotFoundError:
            return ""

    def add_entry(self, entry: str) -> None:
        # Simplistic append for MVP. In reality, we'd parse and insert into the correct section.
        content = self.get_index()
        
        # Rimuovi il placeholder se esiste
        placeholder = "*Nessuna fonte indicizzata al momento.*"
        if placeholder in content:
            content = content.replace(placeholder, "")
            
        if entry not in content:
            content = content.rstrip() + f"\n\n{entry}\n"
            self.file_service.write_file(self.index_file_path, content)
