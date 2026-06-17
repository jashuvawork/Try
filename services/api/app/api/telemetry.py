"""Telemetry endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.services.upstox import get_websocket_status

router = APIRouter()


@router.get("/api/telemetry")
async def telemetry() -> dict[str, object]:
    settings = get_settings()
    return {
        "upstox_websocket": get_websocket_status(),
        "upstox_oauth": {
            "redirect_url_configured": bool(settings.upstox_redirect_url),
            "client_id_configured": bool(settings.upstox_client_id),
        },
    }
