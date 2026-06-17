from services.api.app.services.market_state import MarketContext, previous_range


def score_structure_break(context: MarketContext) -> dict:
    previous_high, previous_low = previous_range(context.candles)
    close = context.candles[-1].close
    broke_high = close > previous_high
    broke_low = close < previous_low
    score = 92 if broke_high else 88 if broke_low else 35
    return {"score": score, "previous_15m_high": round(previous_high, 2), "previous_15m_low": round(previous_low, 2), "break_direction": "HIGH" if broke_high else "LOW" if broke_low else "NONE"}
