from services.api.app.services.market_state import MarketContext, premium_acceleration_stats


def score_premium_acceleration(context: MarketContext) -> dict:
    stats = premium_acceleration_stats(context.candles)
    score = min(100, max(0, 55 + stats["z_score"] * 12 + max(stats["roc_5"], 0) * 1.8))
    return {"score": round(score, 2), **stats}
