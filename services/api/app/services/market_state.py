from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from statistics import mean, pstdev


@dataclass(frozen=True)
class OptionCandle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    open_interest: int
    bid: float
    ask: float


@dataclass(frozen=True)
class MarketContext:
    symbol: str
    instrument: str
    direction: str
    current_premium: float
    candles: list[OptionCandle]
    pcr: float
    pcr_previous: float
    call_oi_change: int
    put_oi_change: int
    news_impact: float
    news_classification: str
    ai_confidence: float
    session_time_ist: str


def sample_context() -> MarketContext:
    closes = [49, 50, 51, 50, 52, 53, 51, 54, 55, 57, 60, 64, 67, 72, 78, 92, 88, 73, 66, 68]
    volumes = [18000, 21000, 24000, 19000, 22000, 26000, 23000, 30000, 36000, 41000, 52000, 69000, 74000, 98000, 140000, 420000, 380000, 210000, 150000, 132000]
    oi = [900000, 902000, 904000, 905000, 908000, 912000, 913500, 918000, 925000, 934000, 946000, 961000, 980000, 1004000, 1039000, 1110000, 1145000, 1158000, 1166000, 1170000]
    candles: list[OptionCandle] = []
    base = datetime(2026, 6, 15, 15, 0, tzinfo=timezone.utc)
    previous = closes[0]
    for index, close in enumerate(closes):
        opened = previous
        high = max(opened, close) + (2.5 if index == 15 else 1.2)
        low = min(opened, close) - 1.0
        candles.append(OptionCandle(base.replace(minute=index), opened, high, low, close, volumes[index], oi[index], close - 0.35, close + 0.45))
        previous = close
    return MarketContext(
        symbol="NIFTY",
        instrument="NIFTY 23850 PE 16JUN26",
        direction="BEARISH_UNDERLYING_PUT_EXPANSION",
        current_premium=68,
        candles=candles,
        pcr=0.82,
        pcr_previous=1.04,
        call_oi_change=185000,
        put_oi_change=-90000,
        news_impact=76,
        news_classification="Bearish",
        ai_confidence=94,
        session_time_ist="15:16",
    )


def previous_average_volume(candles: list[OptionCandle], lookback: int = 5) -> float:
    if len(candles) <= lookback:
        return mean(c.volume for c in candles[:-1]) if len(candles) > 1 else 0
    return mean(c.volume for c in candles[-lookback - 1:-1])


def previous_range(candles: list[OptionCandle], lookback: int = 15) -> tuple[float, float]:
    window = candles[-lookback - 1:-1] if len(candles) > lookback else candles[:-1]
    return max(c.high for c in window), min(c.low for c in window)


def premium_acceleration_stats(candles: list[OptionCandle]) -> dict[str, float]:
    closes = [c.close for c in candles]
    velocities = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    current_velocity = velocities[-1]
    previous_velocity = velocities[-2]
    acceleration = current_velocity - previous_velocity
    baseline = velocities[-11:-1] if len(velocities) >= 11 else velocities[:-1]
    sigma = pstdev(baseline) if len(baseline) > 1 else 1
    z_score = acceleration / sigma if sigma else 0
    return {
        "velocity": round(current_velocity, 2),
        "acceleration": round(acceleration, 2),
        "z_score": round(z_score, 2),
        "roc_5": round(closes[-1] - closes[-6], 2) if len(closes) >= 6 else round(closes[-1] - closes[0], 2),
    }
