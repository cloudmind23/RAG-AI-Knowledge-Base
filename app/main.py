"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.routes import documents, query, stream
from app.core import vector_store as vs
from app.core.auth import require_api_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up the vector store — loads from disk if index exists, otherwise stays None
    vs.get_vector_store()
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_title,
        version=settings.app_version,
        description=(
            "A Retrieval-Augmented Generation API. "
            "Ingest documents, then ask questions answered by Claude."
        ),
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        documents.router,
        prefix="/api/v1",
        dependencies=[Depends(require_api_key)],
    )
    app.include_router(
        query.router,
        prefix="/api/v1",
        dependencies=[Depends(require_api_key)],
    )
    app.include_router(
        stream.router,
        prefix="/api/v1",
        dependencies=[Depends(require_api_key)],
    )

    @app.get("/health", tags=["health"])
    async def health():
        return {"status": "ok", "version": settings.app_version}

    return app


app = create_app()
