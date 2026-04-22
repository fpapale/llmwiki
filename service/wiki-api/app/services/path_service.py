import os

class PathService:
    def __init__(self, paths_config):
        self.config = paths_config

    def is_safe_path(self, base_dir: str, target_path: str) -> bool:
        abs_base = os.path.abspath(base_dir)
        abs_target = os.path.abspath(target_path)
        return abs_target.startswith(abs_base)

    def get_raw_path(self, filename: str) -> str:
        return os.path.join(self.config.raw_dir, filename)

    def get_wiki_path(self, filename: str) -> str:
        if not filename.endswith('.md'):
            filename += '.md'
        return os.path.join(self.config.wiki_dir, filename)
