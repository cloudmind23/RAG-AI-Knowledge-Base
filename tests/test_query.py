"""Tests for the query and streaming endpoints."""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from langchain_core.documents import Document


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_chain_result(answer: str, docs: list[Document]):
    return {"answer": answer, "context": docs}


SAMPLE_DOCS = [
    Document(page_content="LangChain helps build LLM applications.", metadata={"source": "docs.txt"}),
    Document(page_content="ChromaDB stores and retrieves vector embeddings.", metadata={"source": "docs.txt"}),
]


# ── /query/ ───────────────────────────────────────────────────────────────────

def test_query_success(client, mock_store):
    with patch("app.core.rag.get_vector_store", return_value=mock_store), \
         patch("app.core.rag.ChatAnthropic") as mock_llm_cls, \
         patch("app.core.rag.create_retrieval_chain") as mock_chain_fn:

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = _make_chain_result("LangChain is great.", SAMPLE_DOCS)
        mock_chain_fn.return_value = mock_chain
        mock_llm_cls.return_value = MagicMock()

        resp = client.post("/api/v1/query/", json={"question": "What is LangChain?"})

    assert resp.status_code == 200
    data = resp.json()
    assert data["question"] == "What is LangChain?"
    assert "answer" in data
    assert isinstance(data["sources"], list)


def test_query_without_sources(client, mock_store):
    with patch("app.core.rag.get_vector_store", return_value=mock_store), \
         patch("app.core.rag.ChatAnthropic") as mock_llm_cls, \
         patch("app.core.rag.create_retrieval_chain") as mock_chain_fn:

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = _make_chain_result("LangChain is great.", SAMPLE_DOCS)
        mock_chain_fn.return_value = mock_chain
        mock_llm_cls.return_value = MagicMock()

        resp = client.post("/api/v1/query/", json={
            "question": "What is LangChain?",
            "include_sources": False,
        })

    assert resp.status_code == 200
    assert resp.json()["sources"] == []


def test_query_empty_kb_returns_400(client, empty_store):
    resp = client.post("/api/v1/query/", json={"question": "anything"})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


def test_query_missing_question_fails(client):
    resp = client.post("/api/v1/query/", json={})
    assert resp.status_code == 422


def test_query_k_override(client, mock_store):
    """k parameter should be passed through to the retriever."""
    with patch("app.core.rag.get_vector_store", return_value=mock_store), \
         patch("app.core.rag.ChatAnthropic") as mock_llm_cls, \
         patch("app.core.rag.create_retrieval_chain") as mock_chain_fn:

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = _make_chain_result("answer", SAMPLE_DOCS)
        mock_chain_fn.return_value = mock_chain
        mock_llm_cls.return_value = MagicMock()

        resp = client.post("/api/v1/query/", json={"question": "hi", "k": 2})

    assert resp.status_code == 200
    # Verify the retriever was built with k=2
    mock_store.as_retriever.assert_called_with(search_kwargs={"k": 2})


# ── /query/stream ─────────────────────────────────────────────────────────────

def test_stream_empty_kb_returns_400(client, empty_store):
    resp = client.post("/api/v1/query/stream", json={"question": "hello"})
    assert resp.status_code == 400


async def _fake_astream(messages):
    """Yields fake token chunks."""
    for token in ["Hello", " ", "world", "!"]:
        chunk = MagicMock()
        chunk.content = token
        yield chunk


def test_stream_returns_sse_events(client, mock_store):
    with patch("app.api.routes.stream.ChatAnthropic") as mock_llm_cls, \
         patch("app.api.routes.stream.get_vector_store", return_value=mock_store):

        mock_llm = MagicMock()
        mock_llm.astream = _fake_astream
        mock_llm_cls.return_value = mock_llm

        with client.stream("POST", "/api/v1/query/stream", json={"question": "test"}) as resp:
            assert resp.status_code == 200
            assert "text/event-stream" in resp.headers["content-type"]

            events = []
            for line in resp.iter_lines():
                if line.startswith("event:"):
                    events.append(line.split(":", 1)[1].strip())

            assert "sources" in events
            assert "token" in events
            assert "done" in events
