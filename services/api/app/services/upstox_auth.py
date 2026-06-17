"""Helpers for Upstox OAuth URL generation."""

from __future__ import annotations

from urllib.parse import urlencode

from app.core.config import Settings, get_settings


def build_upstox_authorize_url(state: str | None = None, settings: Settings | None = None) -> str:
    """Build the Upstox authorization URL from backend configuration."""
    settings = settings or get_settings()
    if not settings.upstox_client_id:
        raise ValueError("UPSTOX_CLIENT_ID is not configured")
    if not settings.upstox_redirect_url:
        raise ValueError("UPSTOX_REDIRECT_URL is not configured")

    params = {
        "response_type": "code",
        "redirect_uri": settings.upstox_redirect_url,
        "client_id": settings.upstox_client_id,
    }
    if state:
        params["state"] = state
    return f"{settings.upstox_authorize_url}?{urlencode(params)}"
