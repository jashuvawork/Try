"""Upstox OAuth helper endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse

from app.services.upstox_auth import build_upstox_authorize_url

router = APIRouter()


def _configured_auth_url(state: str | None = None) -> str:
    try:
        return build_upstox_authorize_url(state)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/api/upstox/auth-url")
async def upstox_auth_url(state: str | None = Query(default=None)) -> dict[str, str]:
    """Return the backend-generated Upstox OAuth URL for frontend use."""
    return {"auth_url": _configured_auth_url(state)}


@router.get("/api/upstox/authorize")
async def redirect_to_upstox(state: str | None = Query(default=None)) -> RedirectResponse:
    """Redirect a browser to Upstox OAuth using backend config."""
    return RedirectResponse(_configured_auth_url(state), status_code=302)
