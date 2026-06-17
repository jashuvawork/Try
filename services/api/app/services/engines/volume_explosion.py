from services.api.app.services.market_state import MarketContext, previous_average_volume


def score_volume_explosion(context: MarketContext) -> dict:
    current = context.candles[-1].volume
    average = previous_average_volume(context.candles)
    multiple = current / average if average else 0
    score = min(100, multiple / 3 * 85 + max(0, multiple - 3) * 10)
    return {"score": round(score, 2), "current_volume": current, "previous_5m_average": round(average, 2), "volume_multiple": round(multiple, 2)}
