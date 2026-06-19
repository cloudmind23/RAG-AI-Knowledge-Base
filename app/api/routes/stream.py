"""Streaming query endpoint — streams Claude tokens via Server-Sent Events."""
import json
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_anthropic import ChatAnthropic
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from app.config import get_settings
from app.core import vector_store as vs
from app.models import QueryRequest

router = APIRouter(prefix="/query", tags=["query"])

_SYSTEM_PROMPT = """\
You are a helpful assistant that answers questions using only the provided context.
If the context does not contain enough information, say so clearly.
Do not hallucinate or make up information.

Context:
{context}
"""


async def _sse_generator(question: str, k: int) -> AsyncGenerator[str, None]:
    """Retrieve chunks, then stream the LLM answer as SSE events."""
    settings = get_settings()
    store = vs.get_vector_store()

    # --- Retrieval (sync, fast) ---
    docs: list[Document] = store.similarity_search(question, k=k)

    # Emit source metadata before the answer stream
    sources = [
        {"content": d.page_content[:300], "source": d.metadata.get("source"), "metadata": d.metadata}
        for d in docs
    ]
    yield f"event: sources\ndata: {json.dumps(sources)}\n\n"

    # --- Streaming generation ---
    llm = ChatAnthropic(
        model=settings.claude_model,
        anthropic_api_key=settings.anthropic_api_key,
        streaming=True,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", _SYSTEM_PROMPT),
        ("human", "{input}"),
    ])

    context_text = "\n\n---\n\n".join(d.page_content for d in docs)
    messages = prompt.format_messages(input=question, context=context_text)

    async for chunk in llm.astream(messages):
        token = chunk.content
        if token:
            yield f"event: token\ndata: {json.dumps({'token': token})}\n\n"

    yield "event: done\ndata: {}\n\n"


@router.post("/stream")
async def stream_query(body: QueryRequest):
    """
    Stream Claude's answer token-by-token using Server-Sent Events.

    Event types:
    - `sources`  — fired once before generation; contains retrieved chunks
    - `token`    — fired per token; `data.token` contains the text piece
    - `done`     — fired once when generation is complete
    """
    settings = get_settings()

    if vs.document_count() == 0:
        raise HTTPException(
            status_code=400,
            detail="Knowledge base is empty. Ingest documents first.",
        )

    k = body.k or settings.retrieval_k

    return StreamingResponse(
        _sse_generator(body.question, k),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable nginx buffering
        },
    )
