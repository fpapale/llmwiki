import os
import yaml
from pydantic_settings import BaseSettings
from pydantic import Field, BaseModel

class AppConfig(BaseModel):
    name: str = "wiki-api"
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "INFO"

class PathsConfig(BaseModel):
    vault_root: str = "../../"
    raw_dir: str = "../../raw"
    wiki_dir: str = "../../wiki"
    schema_dir: str = "../../wiki"
    agent_file: str = "../../wiki/AGENT.MD"
    index_file: str = "../../wiki/index.md"
    log_file: str = "../../wiki/log.md"

class LLMConfig(BaseModel):
    enabled: bool = True
    provider: str = "openai"
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"
    api_key_env: str = "OPENAI_API_KEY"
    timeout_seconds: int = 120

class FeaturesConfig(BaseModel):
    enable_fallback_query: bool = True
    enable_mock_llm: bool = True

class Settings(BaseSettings):
    app: AppConfig = Field(default_factory=AppConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    features: FeaturesConfig = Field(default_factory=FeaturesConfig)
    
    # Secrets that will be picked up from the .env or environment
    openai_api_key: str = Field(default="mock_key", alias="OPENAI_API_KEY")

def load_config() -> Settings:
    config_path = os.environ.get("WIKI_API_CONFIG_PATH", "../../runtime/config/config.yaml")
    secrets_path = os.environ.get("WIKI_API_SECRETS_PATH", "../../runtime/config/secrets.env")

    # Load secrets from dotenv if path exists
    from dotenv import load_dotenv
    if os.path.exists(secrets_path):
        load_dotenv(secrets_path)

    # Load YAML config
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f) or {}
    else:
        yaml_data = {}

    settings = Settings(
        app=AppConfig(**yaml_data.get("app", {})),
        paths=PathsConfig(**yaml_data.get("paths", {})),
        llm=LLMConfig(**yaml_data.get("llm", {})),
        features=FeaturesConfig(**yaml_data.get("features", {}))
    )

    # Resolve paths relative to the config file location
    base_dir = os.path.dirname(os.path.abspath(config_path))
    
    def resolve_path(p: str) -> str:
        if os.path.isabs(p):
            return os.path.normpath(p)
        return os.path.normpath(os.path.join(base_dir, p))

    settings.paths.vault_root = resolve_path(settings.paths.vault_root)
    settings.paths.raw_dir = resolve_path(settings.paths.raw_dir)
    settings.paths.wiki_dir = resolve_path(settings.paths.wiki_dir)
    settings.paths.schema_dir = resolve_path(settings.paths.schema_dir)
    settings.paths.agent_file = resolve_path(settings.paths.agent_file)
    settings.paths.index_file = resolve_path(settings.paths.index_file)
    settings.paths.log_file = resolve_path(settings.paths.log_file)

    return settings

settings = load_config()
