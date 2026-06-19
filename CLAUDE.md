# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt   # or: bash install.sh

# Run the API server (hot-reload)
uvicorn app.main:app --reload

# Run all tests (no API key or network required)
pytest

# Run a single test file
pytest tests/test_auth.py

# Ingest NBA demo data (requires server running on localhost:8000)
python ingest_nba.py
```

The Swagger UI is available at `http://localhost:8000/docs` when the server is running.

## Architecture

This is a **Retrieval-Augmented Generation (RAG) API** built with FastAPI. Documents are ingested, chunked, embedded, and stored in a FAISS vector index. Queries retrieve the top-k relevant chunks, which are passed as context to Claude to generate grounded answers.

### Request flow

```text
POST /api/v1/documents/ingest/*
  → document_loader.py (load + chunk)
  → vector_store.py (embed with all-MiniLM-L6-v2 + add to FAISS index + persist to disk)

POST /api/v1/query/
  → rag.py (build LangChain retrieval chain → retrieve → generate with Claude)
  → returns QueryResponse with answer + source chunks

POST /api/v1/query/stream
  → stream.py (manual: similarity_search → Claude astream → SSE events)
  → emits: `sources` event, then `token` events, then `done`
```

### Key modules

- **`app/config.py`** — Pydantic-settings `Settings` class loaded from `.env`. Cached via `@lru_cache` as `get_settings()`. All configurable values (model, chunk size, retrieval k, auth keys, persist dir) live here.
- **`app/core/vector_store.py`** — Module-level FAISS singleton (`_store`). Loaded from `./data/faiss_index/` at startup (via the `lifespan` hook in `main.py`) and persisted to disk on every write. Embeddings use the local `all-MiniLM-L6-v2` model (~90 MB, downloads to `~/.cache/` on first use).
- **`app/core/rag.py`** — Builds a LangChain `create_retrieval_chain` for non-streaming queries. The streaming endpoint (`stream.py`) does NOT use this chain — it manually calls `similarity_search` then `llm.astream`.
- **`app/core/auth.py`** — FastAPI dependency `require_api_key` reads the `X-API-Key` header. Auth is **disabled** when `API_KEYS` is empty/unset, which is the default for local dev.
- **`app/utils/document_loader.py`** — Handles file ingestion (PDF via PyPDF, DOCX via Docx2txt, TXT/MD via TextLoader) and text chunking via `RecursiveCharacterTextSplitter`.

### Configuration (`.env`)

Copy `.env.example` to `.env`. The only required field is `ANTHROPIC_API_KEY`. All other fields have defaults. `API_KEYS` accepts a comma-separated list; leave it empty to disable auth.

### Testing

Tests mock both FAISS and Anthropic entirely — no real API key or network access needed. `tests/conftest.py` patches `get_settings` at each module's import path (e.g. `app.core.rag.get_settings`, not just `app.config.get_settings`). When adding new modules that call `get_settings()`, add a corresponding monkeypatch entry in `conftest.py`'s `override_settings` fixture to keep tests isolated.
