# RAG Knowledge Base API

A self-hosted Retrieval-Augmented Generation (RAG) API. Ingest your documents, then ask natural-language questions, the API finds the most relevant passages and uses Claude to generate a grounded answer backed by your data.

## How it works

1. **Ingest** — upload files (PDF, DOCX, TXT, MD) or POST raw text. Documents are chunked and embedded using a local sentence-transformer model (`all-MiniLM-L6-v2`, ~90 MB, downloads automatically on first use).
2. **Store** — embeddings are persisted in a local FAISS index (`./data/faiss_index/`) that survives server restarts.
3. **Query** — ask a question; the API retrieves the top-k most relevant chunks and sends them as context to Claude, which generates an answer without hallucinating beyond the provided material. A streaming endpoint delivers tokens in real time via Server-Sent Events.

## Features

- **File ingestion**: PDF, DOCX, DOC, TXT, MD
- **Text ingestion**: POST raw text with optional metadata
- **Batch query**: returns a complete answer + source chunks
- **Streaming query**: token-by-token SSE stream (`sources` → `token`… → `done`)
- **Optional API key auth**: set `API_KEYS` in `.env`; leave it empty to disable (useful for local dev)
- **Fully local embeddings**: no extra API key or external service required for embedding
- **Interactive docs**: Swagger UI at `/docs`, ReDoc at `/redoc`

## Requirements

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

```bash
git clone <your-repo-url>
cd rag-knowledge-base

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY
```

### `.env` options

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | *(required)* | Your Anthropic API key |
| `CLAUDE_MODEL` | `claude-opus-4-8` | Claude model to use for generation |
| `API_KEYS` | *(empty — auth disabled)* | Comma-separated valid API keys for the `X-API-Key` header |
| `CHUNK_SIZE` | `1000` | Max characters per document chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between consecutive chunks |
| `RETRIEVAL_K` | `5` | Number of chunks to retrieve per query |
| `DEBUG` | `false` | Enable debug logging |

## Running

```bash
uvicorn app.main:app --reload
```

The API is now available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

## API endpoints

All endpoints (except `/health`) are prefixed with `/api/v1` and require an `X-API-Key` header if `API_KEYS` is set.

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/documents/ingest/text` | Ingest raw text |
| `POST` | `/api/v1/documents/ingest/file` | Upload and ingest a file |
| `GET` | `/api/v1/documents/stats` | Number of vectors in the index |
| `DELETE` | `/api/v1/documents/all` | Wipe the entire knowledge base |
| `POST` | `/api/v1/query/` | Ask a question (full response) |
| `POST` | `/api/v1/query/stream` | Ask a question (SSE stream) |

## Example usage

### Ingest text

```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest/text \
  -H "Content-Type: application/json" \
  -d '{"content": "FastAPI is a modern web framework for Python.", "source": "notes.txt"}'
```

### Ingest a file

```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest/file \
  -F "file=@report.pdf"
```

### Query

```bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?", "include_sources": true}'
```

### Stream a query

```bash
curl -N -X POST http://localhost:8000/api/v1/query/stream \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?"}'
```

### Load the NBA demo dataset

A script is included to populate the knowledge base with 2026 NBA Playoff data (useful for quickly testing the API):

```bash
python ingest_nba.py
```

## Running tests

Tests mock all external I/O (FAISS, Anthropic) — no API key or network access required.

```bash
pytest
```

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [LangChain](https://www.langchain.com/) — RAG orchestration
- [FAISS](https://github.com/facebookresearch/faiss) — vector similarity search
- [sentence-transformers](https://www.sbert.net/) — local embeddings (`all-MiniLM-L6-v2`)
- [Anthropic Claude](https://www.anthropic.com/) — answer generation
