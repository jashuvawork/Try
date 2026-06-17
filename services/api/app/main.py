"""FastAPI application factory for the API service."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.telemetry import router as telemetry_router
from app.api.upstox import router as upstox_router

app = FastAPI(title="Try API")
app.include_router(telemetry_router)
app.include_router(upstox_router)
