from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Anthropic
    anthropic_api_key: str
    claude_model: str = "claude-opus-4-8"

    # FAISS vector store
    persist_dir: str = "./data/faiss_index"

    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Retrieval
    retrieval_k: int = 5  # top-k documents to retrieve

    # Auth — comma-separated list of valid API keys; empty = auth disabled
    api_keys: list[str] = []

    @field_validator("api_keys", mode="before")
    @classmethod
    def _parse_api_keys(cls, v):
        if isinstance(v, str):
            return [k.strip() for k in v.split(",") if k.strip()]
        return v

    # App
    app_title: str = "RAG Knowledge Base API"
    app_version: str = "0.1.0"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
