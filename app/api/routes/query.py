"""Query / ask endpoint."""
from fastapi import APIRouter, HTTPException
from app.models import QueryRequest, QueryResponse
from app.core.rag import run_rag_query
from app.core import vector_store as vs

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/", response_model=QueryResponse)
async def ask(body: QueryRequest):
    """Ask a question — retrieves relevant chunks then generates an answer with Claude."""
    if vs.document_count() == 0:
        raise HTTPException(
            status_code=400,
            detail="Knowledge base is empty. Ingest documents first.",
        )

    return run_rag_query(
        question=body.question,
        k=body.k,
        include_sources=body.include_sources,
    )
