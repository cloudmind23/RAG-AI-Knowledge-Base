"""Helpers to load and split documents from various sources."""
import tempfile
import os
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)

from app.config import get_settings


def get_splitter() -> RecursiveCharacterTextSplitter:
    settings = get_settings()
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        add_start_index=True,
    )


def split_text(content: str, metadata: dict | None = None) -> list[Document]:
    """Split raw text into chunks."""
    docs = [Document(page_content=content, metadata=metadata or {})]
    return get_splitter().split_documents(docs)


def load_and_split_file(file_bytes: bytes, filename: str, metadata: dict | None = None) -> list[Document]:
    """Save uploaded bytes to a temp file, load with the appropriate loader, then split."""
    suffix = Path(filename).suffix.lower()
    extra_meta = {"source": filename, **(metadata or {})}

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        loader = _pick_loader(tmp_path, suffix)
        docs = loader.load()
        for doc in docs:
            doc.metadata.update(extra_meta)
        return get_splitter().split_documents(docs)
    finally:
        os.unlink(tmp_path)


def _pick_loader(path: str, suffix: str):
    match suffix:
        case ".pdf":
            return PyPDFLoader(path)
        case ".docx" | ".doc":
            return Docx2txtLoader(path)
        case ".md":
            return TextLoader(path, encoding="utf-8")
        case _:  # .txt and everything else
            return TextLoader(path, encoding="utf-8")
