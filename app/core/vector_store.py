"""FAISS-backed vector store with disk persistence."""
import shutil
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from app.config import get_settings

# Module-level singleton — survives across requests in a single process
_store: FAISS | None = None

# Local embedding model (~90 MB, downloads once on first use)
_EMBED_MODEL = "all-MiniLM-L6-v2"


def _embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=_EMBED_MODEL)


def _index_path() -> Path:
    return Path(get_settings().persist_dir)


def get_vector_store() -> FAISS | None:
    """Return the in-memory store, loading from disk if needed. None = empty."""
    global _store
    if _store is None:
        _store = _try_load()
    return _store


def add_documents(docs: list[Document]) -> None:
    """Add chunks and persist to disk."""
    global _store
    emb = _embeddings()
    if _store is None:
        _store = FAISS.from_documents(docs, emb)
    else:
        _store.add_documents(docs)
    _save()


def document_count() -> int:
    store = get_vector_store()
    return 0 if store is None else store.index.ntotal


def delete_all() -> int:
    """Wipe the index from memory and disk. Returns number of deleted vectors."""
    global _store
    count = document_count()
    _store = None
    path = _index_path()
    if path.exists():
        shutil.rmtree(path)
    return count


# ── Internal helpers ──────────────────────────────────────────────────────────

def _try_load() -> FAISS | None:
    path = _index_path()
    if (path / "index.faiss").exists():
        return FAISS.load_local(
            str(path),
            _embeddings(),
            allow_dangerous_deserialization=True,
        )
    return None


def _save() -> None:
    path = _index_path()
    path.mkdir(parents=True, exist_ok=True)
    if _store:
        _store.save_local(str(path))
