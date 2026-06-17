"""Upstox Market Data Websocket V3 streaming service."""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass
from importlib import import_module
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Callable, Iterable, Mapping

from app.core.config import Settings, get_settings

LOGGER = logging.getLogger("app.services.upstox")
NIFTY_STREAM = "ticks:nifty_options"
SENSEX_STREAM = "ticks:sensex_options"


@dataclass(slots=True)
class NormalizedTick:
    instrument_key: str
    ltp: float | None
    volume: int | None
    oi: int | None
    bid_price: float | None
    ask_price: float | None
    bid_qty: int | None
    ask_qty: int | None
    timestamp: str


@dataclass(slots=True)
class UpstoxWebsocketStatus:
    connected: bool = False
    last_tick_time: str | None = None
    subscribed_instruments: tuple[str, ...] = ()
    reconnect_count: int = 0
    last_disconnect_reason: str | None = None


_STATUS = UpstoxWebsocketStatus()


def get_websocket_status() -> dict[str, Any]:
    """Return telemetry-safe websocket status."""
    return asdict(_STATUS)


def _json_log(level: int, event: str, **fields: Any) -> None:
    LOGGER.log(level, json.dumps({"event": event, **fields}, default=str))


def _millis_to_iso(value: Any) -> str:
    try:
        return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc).isoformat()
    except (TypeError, ValueError):
        return datetime.now(timezone.utc).isoformat()


def _first_depth(feed: Mapping[str, Any]) -> Mapping[str, Any]:
    for key in ("marketLevel", "marketOHLC", "depth"):
        levels = feed.get(key) or {}
        quotes = levels.get("bidAskQuote") if isinstance(levels, Mapping) else None
        if quotes:
            return quotes[0]
    quotes = feed.get("bidAskQuote")
    return quotes[0] if quotes else {}


def normalize_tick(instrument_key: str, feed: Mapping[str, Any], current_ts: Any) -> NormalizedTick:
    """Normalize a decoded Upstox feed payload into the internal tick model."""
    ltpc = feed.get("ltpc") or feed.get("fullFeed", {}).get("ltpc") or {}
    details = feed.get("firstLevelWithGreeks") or feed.get("ff", {}) or feed
    depth = _first_depth(details)
    return NormalizedTick(
        instrument_key=instrument_key,
        ltp=ltpc.get("ltp") or details.get("ltp"),
        volume=details.get("vtt") or details.get("volume"),
        oi=details.get("oi"),
        bid_price=depth.get("bidP") or depth.get("bp") or details.get("bidPrice"),
        ask_price=depth.get("askP") or depth.get("ap") or details.get("askPrice"),
        bid_qty=depth.get("bidQ") or depth.get("bq") or details.get("bidQty"),
        ask_qty=depth.get("askQ") or depth.get("aq") or details.get("askQty"),
        timestamp=_millis_to_iso(ltpc.get("ltt") or current_ts),
    )


def _stream_for_instrument(instrument_key: str) -> str:
    return SENSEX_STREAM if instrument_key.startswith("BSE_FO|") else NIFTY_STREAM


async def _publish_tick(redis: Any, tick: NormalizedTick) -> None:
    await redis.xadd(_stream_for_instrument(tick.instrument_key), asdict(tick))


def _build_protobuf_decoder(module_name: str) -> Callable[[bytes], Mapping[str, Any]]:
    """Build a decoder for Upstox Market Data Feed V3 protobuf frames."""
    from google.protobuf.json_format import MessageToDict

    proto_module = import_module(module_name)
    response_class = getattr(proto_module, "FeedResponse")

    def decode(message: bytes) -> Mapping[str, Any]:
        response = response_class()
        response.ParseFromString(message)
        return MessageToDict(response, preserving_proto_field_name=False)

    return decode


async def _decode_messages(
    websocket: Any, protobuf_decoder: Callable[[bytes], Mapping[str, Any]]
) -> AsyncIterator[Mapping[str, Any]]:
    """Yield decoded Upstox V3 messages from protobuf binary or JSON frames."""
    async for message in websocket:
        if isinstance(message, bytes):
            yield protobuf_decoder(message)
            continue
        yield json.loads(message)


async def _subscribe(websocket: Any, instruments: Iterable[str]) -> None:
    payload = {
        "guid": uuid.uuid4().hex,
        "method": "sub",
        "data": {"mode": "full", "instrumentKeys": list(instruments)},
    }
    await websocket.send(json.dumps(payload).encode("utf-8"))


async def stream_market_data(settings: Settings | None = None, redis: Any | None = None) -> None:
    """Connect to Upstox Websocket V3, normalize ticks, and publish to Redis streams."""
    import redis.asyncio as redis_async
    import websockets

    settings = settings or get_settings()
    redis = redis or redis_async.from_url(settings.redis_url, decode_responses=True)
    protobuf_decoder = _build_protobuf_decoder(settings.upstox_feed_proto_module)
    instruments = tuple(settings.upstox_instrument_subscriptions)
    _STATUS.subscribed_instruments = instruments
    backoff = 1

    while True:
        try:
            headers = {"Authorization": f"Bearer {settings.upstox_access_token}", "Accept": "*/*"}
            async with websockets.connect(
                settings.upstox_websocket_url,
                additional_headers=headers,
                ping_interval=20,
                ping_timeout=20,
                max_queue=2048,
            ) as websocket:
                _STATUS.connected = True
                _STATUS.last_disconnect_reason = None
                backoff = 1
                await _subscribe(websocket, instruments)
                _json_log(logging.INFO, "upstox_connected", subscribed_instruments=instruments)

                async for payload in _decode_messages(websocket, protobuf_decoder):
                    for instrument_key, feed in (payload.get("feeds") or {}).items():
                        tick = normalize_tick(instrument_key, feed, payload.get("currentTs"))
                        await _publish_tick(redis, tick)
                        _STATUS.last_tick_time = tick.timestamp
        except Exception as exc:  # reconnect loop must catch transport/protobuf errors
            _STATUS.connected = False
            _STATUS.reconnect_count += 1
            _STATUS.last_disconnect_reason = str(exc)
            _json_log(
                logging.WARNING,
                "upstox_disconnected",
                reason=str(exc),
                reconnect_count=_STATUS.reconnect_count,
                retry_in_seconds=backoff,
            )
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
