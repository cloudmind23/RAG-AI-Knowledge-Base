from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Ingest ────────────────────────────────────────────────────────────────────

class IngestTextRequest(BaseModel):
    """Ingest raw text with optional metadata."""
    content: str = Field(..., min_length=1, description="Text content to store")
    source: Optional[str] = Field(None, description="Source label (URL, filename, etc.)")
    metadata: Optional[dict] = Field(default_factory=dict, description="Arbitrary metadata")


class IngestResponse(BaseModel):
    message: str
    document_count: int
    chunk_count: int


# ── Query ─────────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural-language question")
    k: Optional[int] = Field(None, ge=1, le=20, description="Override retrieval_k")
    include_sources: bool = Field(True, description="Include source chunks in response")


class SourceChunk(BaseModel):
    content: str
    source: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    relevance_score: Optional[float] = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk] = Field(default_factory=list)
    model: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Collection management ─────────────────────────────────────────────────────

class CollectionStats(BaseModel):
    collection_name: str
    document_count: int


class DeleteResponse(BaseModel):
    message: str
    deleted_count: int
