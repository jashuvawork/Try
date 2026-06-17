from services.api.app.services.market_state import MarketContext


def score_option_chain_bias(context: MarketContext) -> dict:
    pcr_shift = context.pcr - context.pcr_previous
    bearish = context.call_oi_change > 0 and context.put_oi_change < 0 and pcr_shift < 0
    bullish = context.put_oi_change > 0 and context.call_oi_change < 0 and pcr_shift > 0
    bearish_score = 88 if bearish else 34
    bullish_score = 88 if bullish else 28
    return {
        "pcr": context.pcr,
        "pcr_shift": round(pcr_shift, 2),
        "call_oi_change": context.call_oi_change,
        "put_oi_change": context.put_oi_change,
        "bullish_score": bullish_score,
        "bearish_score": bearish_score,
        "neutral_score": 100 - max(bullish_score, bearish_score),
        "aligned": bearish if "BEARISH" in context.direction else bullish,
    }
