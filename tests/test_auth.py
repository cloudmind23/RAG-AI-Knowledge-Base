"""Tests for API key authentication."""
import pytest
from tests.conftest import AUTH_HEADER, VALID_KEY


def test_no_key_returns_401(authed_client):
    resp = authed_client.post("/api/v1/query/", json={"question": "hello"})
    assert resp.status_code == 401


def test_wrong_key_returns_403(authed_client):
    resp = authed_client.post(
        "/api/v1/query/",
        json={"question": "hello"},
        headers={"X-API-Key": "wrong-key"},
    )
    assert resp.status_code == 403


def test_valid_key_passes_auth(authed_client, mock_store):
    """Valid key should reach the route (we'll get 400 from empty store, not 401/403)."""
    mock_store.index.ntotal = 0
    resp = authed_client.post(
        "/api/v1/query/",
        json={"question": "hello"},
        headers=AUTH_HEADER,
    )
    # Auth passed — error is from empty KB, not auth
    assert resp.status_code == 400
    assert resp.status_code != 401
    assert resp.status_code != 403


def test_health_endpoint_requires_no_key(authed_client):
    resp = authed_client.get("/health")
    assert resp.status_code == 200
