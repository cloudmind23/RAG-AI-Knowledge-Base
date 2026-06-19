"""Document ingestion endpoints."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Annotated

from app.config import Settings, get_settings
from app.models import IngestTextRequest, IngestResponse, CollectionStats, DeleteResponse
from app.core import vector_store as vs
from app.utils.document_loader import split_text, load_and_split_file

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/ingest/text", response_model=IngestResponse, status_code=201)
async def ingest_text(
    body: IngestTextRequest,
    settings: Annotated[Settings, Depends(get_settings)],
):
    """Ingest raw text into the knowledge base."""
    meta = {"source": body.source or "manual", **(body.metadata or {})}
    chunks = split_text(body.content, meta)

    if not chunks:
        raise HTTPException(status_code=422, detail="No chunks produced from provided text.")

    vs.add_documents(chunks)

    return IngestResponse(
        message="Text ingested successfully.",
        document_count=1,
        chunk_count=len(chunks),
    )


@router.post("/ingest/file", response_model=IngestResponse, status_code=201)
async def ingest_file(
    file: Annotated[UploadFile, File(description="PDF, DOCX, TXT, or MD file")],
):
    """Upload and ingest a document file."""
    allowed = {".pdf", ".docx", ".doc", ".txt", ".md"}
    suffix = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if suffix not in allowed:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{suffix}'. Allowed: {', '.join(allowed)}",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=422, detail="Uploaded file is empty.")

    chunks = load_and_split_file(file_bytes, file.filename)

    if not chunks:
        raise HTTPException(status_code=422, detail="No content could be extracted from the file.")

    vs.add_documents(chunks)

    return IngestResponse(
        message=f"File '{file.filename}' ingested successfully.",
        document_count=1,
        chunk_count=len(chunks),
    )


@router.get("/stats", response_model=CollectionStats)
async def collection_stats(settings: Annotated[Settings, Depends(get_settings)]):
    """Return the number of vectors stored in the index."""
    return CollectionStats(
        collection_name="faiss_index",
        document_count=vs.document_count(),
    )


@router.delete("/all", response_model=DeleteResponse)
async def delete_all_documents():
    """⚠️  Delete every document in the knowledge base."""
    deleted = vs.delete_all()
    return DeleteResponse(message="All documents deleted.", deleted_count=deleted)
