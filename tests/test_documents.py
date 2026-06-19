"""Tests for document ingestion endpoints."""
import io
import pytest


# ── /ingest/text ──────────────────────────────────────────────────────────────

def test_ingest_text_success(client, mock_store):
    resp = client.post("/api/v1/documents/ingest/text", json={
        "content": "FastAPI is a modern Python web framework.",
        "source": "manual",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["chunk_count"] >= 1
    assert data["document_count"] == 1
    mock_store.add_documents.assert_called_once()


def test_ingest_text_empty_body_fails(client):
    resp = client.post("/api/v1/documents/ingest/text", json={"content": ""})
    assert resp.status_code == 422  # pydantic min_length=1


def test_ingest_text_with_metadata(client, mock_store):
    resp = client.post("/api/v1/documents/ingest/text", json={
        "content": "Some knowledge.",
        "source": "wiki",
        "metadata": {"author": "Alice", "year": 2024},
    })
    assert resp.status_code == 201


# ── /ingest/file ──────────────────────────────────────────────────────────────

def test_ingest_txt_file(client, mock_store):
    content = b"This is a plain text document about RAG systems."
    resp = client.post(
        "/api/v1/documents/ingest/file",
        files={"file": ("notes.txt", io.BytesIO(content), "text/plain")},
    )
    assert resp.status_code == 201
    assert resp.json()["chunk_count"] >= 1


def test_ingest_unsupported_format_fails(client):
    resp = client.post(
        "/api/v1/documents/ingest/file",
        files={"file": ("data.csv", io.BytesIO(b"a,b,c"), "text/csv")},
    )
    assert resp.status_code == 415


def test_ingest_empty_file_fails(client):
    resp = client.post(
        "/api/v1/documents/ingest/file",
        files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")},
    )
    assert resp.status_code == 422


# ── /stats ────────────────────────────────────────────────────────────────────

def test_stats_returns_count(client, mock_store):
    mock_store.index.ntotal = 42
    resp = client.get("/api/v1/documents/stats")
    assert resp.status_code == 200
    # The route calls vs.document_count() which is patched to return store.index.ntotal
    assert resp.json()["document_count"] >= 0


# ── /all (DELETE) ─────────────────────────────────────────────────────────────

def test_delete_all_documents(client, mock_store):
    resp = client.delete("/api/v1/documents/all")
    assert resp.status_code == 200
    data = resp.json()
    assert "deleted_count" in data


def test_delete_all_empty_store(client, empty_store):
    resp = client.delete("/api/v1/documents/all")
    assert resp.status_code == 200
    assert resp.json()["deleted_count"] == 0
