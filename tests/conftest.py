"""
Shared fixtures — all external I/O (FAISS, Anthropic) is mocked so the
test suite runs without network access or real API keys.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from langchain_core.documents import Document

# ---------------------------------------------------------------------------
# Settings override — must happen before the app is imported
# ---------------------------------------------------------------------------
from app.config import get_settings, Settings


def _test_settings(**overrides):
    return Settings(
        anthropic_api_key="test-key",
        api_keys=["valid-test-key"],
        persist_dir="/tmp/test_faiss",
        **overrides,
    )


# ---------------------------------------------------------------------------
# Mock FAISS store
# ---------------------------------------------------------------------------
def make_mock_store(doc_count: int = 3, search_results: list[Document] | None = None):
    """Return a MagicMock shaped like a FAISS store."""
    docs = search_results or [
        Document(page_content="LangChain is a framework for LLM apps.", metadata={"source": "test.txt"}),
        Document(page_content="FAISS is a vector index library.", metadata={"source": "test.txt"}),
    ]
    store = MagicMock()
    # FAISS exposes vector count via store.index.ntotal
    store.index = MagicMock()
    store.index.ntotal = doc_count
    store.add_documents.return_value = None
    store.similarity_search.return_value = docs
    store.as_retriever.return_value = MagicMock(
        invoke=MagicMock(return_value=docs),
    )
    return store


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def override_settings(monkeypatch):
    """Replace get_settings with test settings for every test."""
    ts = _test_settings()
    monkeypatch.setattr("app.config.get_settings", lambda: ts)
    monkeypatch.setattr("app.core.auth.get_settings", lambda: ts)
    monkeypatch.setattr("app.core.rag.get_settings", lambda: ts)
    monkeypatch.setattr("app.api.routes.documents.get_settings", lambda: ts)
    monkeypatch.setattr("app.api.routes.query.get_settings", lambda: ts)
    monkeypatch.setattr("app.api.routes.stream.get_settings", lambda: ts)


@pytest.fixture()
def mock_store(monkeypatch):
    """Patch the vector_store module functions to use a mock FAISS instance."""
    store = make_mock_store()

    monkeypatch.setattr("app.core.vector_store.get_vector_store", lambda: store)
    monkeypatch.setattr("app.core.vector_store.document_count", lambda: store.index.ntotal)
    monkeypatch.setattr("app.core.vector_store.add_documents", store.add_documents)
    monkeypatch.setattr("app.core.vector_store.delete_all", lambda: store.index.ntotal)

    # Also patch the `vs` alias used in routes/rag
    import app.core.vector_store as _vs
    monkeypatch.setattr(_vs, "get_vector_store", lambda: store)
    monkeypatch.setattr(_vs, "document_count", lambda: store.index.ntotal)
    monkeypatch.setattr(_vs, "add_documents", store.add_documents)
    monkeypatch.setattr(_vs, "delete_all", lambda: store.index.ntotal)

    return store


@pytest.fixture()
def empty_store(monkeypatch):
    """Return a vector store with no documents (count = 0)."""
    store = make_mock_store(doc_count=0, search_results=[])

    import app.core.vector_store as _vs
    monkeypatch.setattr(_vs, "get_vector_store", lambda: store)
    monkeypatch.setattr(_vs, "document_count", lambda: 0)
    monkeypatch.setattr(_vs, "add_documents", store.add_documents)
    monkeypatch.setattr(_vs, "delete_all", lambda: 0)

    return store


@pytest.fixture()
def client(mock_store):
    """TestClient with auth disabled and a populated store."""
    ts_no_auth = _test_settings(api_keys=[])
    with patch("app.config.get_settings", return_value=ts_no_auth), \
         patch("app.core.auth.get_settings", return_value=ts_no_auth):
        from app.main import create_app
        app = create_app()
        with TestClient(app, raise_server_exceptions=True) as c:
            yield c


@pytest.fixture()
def authed_client(mock_store):
    """TestClient with auth ENABLED (API_KEYS=valid-test-key)."""
    from app.main import create_app
    app = create_app()
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


VALID_KEY = "valid-test-key"
AUTH_HEADER = {"X-API-Key": VALID_KEY}
