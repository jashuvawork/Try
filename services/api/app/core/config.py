"""Application configuration."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import List


DEFAULT_UPSTOX_WS_URL = "wss://api.upstox.com/v3/feed/market-data-feed"
DEFAULT_UPSTOX_AUTHORIZE_URL = "https://api.upstox.com/v2/login/authorization/dialog"
DEFAULT_NIFTY_OPTION_INSTRUMENTS = (
    # Configure exact weekly near-the-money option instrument keys from the
    # current Upstox instruments master. These defaults document the expected
    # segments and keep local development safe until real keys are provided.
    "NSE_FO|NIFTY_WEEKLY_ATM_CE,NSE_FO|NIFTY_WEEKLY_ATM_PE"
)
DEFAULT_SENSEX_OPTION_INSTRUMENTS = (
    "BSE_FO|SENSEX_WEEKLY_ATM_CE,BSE_FO|SENSEX_WEEKLY_ATM_PE"
)


def _csv(value: str | None) -> List[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


class Settings:
    """Environment-backed settings used by the API service."""

    def __init__(self) -> None:
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.upstox_access_token = os.getenv("UPSTOX_ACCESS_TOKEN", "")
        self.upstox_client_id = os.getenv("UPSTOX_CLIENT_ID", "")
        self.upstox_client_secret = os.getenv("UPSTOX_CLIENT_SECRET", "")
        self.upstox_redirect_url = os.getenv("UPSTOX_REDIRECT_URL", "")
        self.upstox_authorize_url = os.getenv(
            "UPSTOX_AUTHORIZE_URL", DEFAULT_UPSTOX_AUTHORIZE_URL
        )
        self.upstox_websocket_url = os.getenv(
            "UPSTOX_WEBSOCKET_URL", DEFAULT_UPSTOX_WS_URL
        )
        self.upstox_feed_proto_module = os.getenv(
            "UPSTOX_FEED_PROTO_MODULE", "MarketDataFeedV3_pb2"
        )
        self.upstox_nifty_option_instruments = _csv(
            os.getenv("UPSTOX_NIFTY_OPTION_INSTRUMENTS", DEFAULT_NIFTY_OPTION_INSTRUMENTS)
        )
        self.upstox_sensex_option_instruments = _csv(
            os.getenv(
                "UPSTOX_SENSEX_OPTION_INSTRUMENTS",
                DEFAULT_SENSEX_OPTION_INSTRUMENTS,
            )
        )

    @property
    def upstox_instrument_subscriptions(self) -> list[str]:
        """All configured option instrument keys to subscribe on the V3 feed."""
        return [
            *self.upstox_nifty_option_instruments,
            *self.upstox_sensex_option_instruments,
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
