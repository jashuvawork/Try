from services.api.app.services.market_state import MarketContext


def score_order_flow(context: MarketContext) -> dict:
    latest = context.candles[-1]
    spread = latest.ask - latest.bid
    mid = (latest.ask + latest.bid) / 2
    spread_pct = spread / mid * 100 if mid else 999
    spread_score = max(0, min(100, 100 - spread_pct * 18))
    buyer_aggression = 84 if latest.close >= latest.open else 58
    seller_aggression = 82 if latest.close < latest.open and "PE" in context.instrument else 42
    imbalance_score = max(buyer_aggression, seller_aggression)
    return {"bid": latest.bid, "ask": latest.ask, "spread": round(spread, 2), "spread_pct": round(spread_pct, 2), "spread_score": round(spread_score, 2), "buyer_aggression": buyer_aggression, "seller_aggression": seller_aggression, "imbalance_score": imbalance_score}
