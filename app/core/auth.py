"""API key authentication.

Reads one or more valid keys from the API_KEYS env var (comma-separated).
Clients must send:  X-API-Key: <key>

If API_KEYS is empty / unset, auth is disabled (useful for local dev).
"""
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

from app.config import get_settings

_header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(api_key: str | None = Security(_header_scheme)) -> str:
    """FastAPI dependency — raises 401/403 if the key is invalid."""
    settings = get_settings()

    # Auth disabled when no keys are configured
    if not settings.api_keys:
        return ""

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header.",
        )

    if api_key not in settings.api_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )

    return api_key
