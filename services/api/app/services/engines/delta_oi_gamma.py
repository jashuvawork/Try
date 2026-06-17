from services.api.app.services.market_state import MarketContext


def score_delta_oi_gamma(context: MarketContext) -> dict:
    latest = context.candles[-1]
    previous = context.candles[-2]
    oi_velocity = latest.open_interest - previous.open_interest
    delta_velocity = min(100, max(0, abs(latest.close - previous.close) * 9 + 52))
    oi_score = min(100, max(0, abs(oi_velocity) / 4500 + 74))
    gamma_score = min(100, max(0, delta_velocity * 0.72 + 18))
    return {"delta_velocity": round(delta_velocity, 2), "oi_velocity": round(oi_score, 2), "raw_oi_change": oi_velocity, "gamma_pressure": round(gamma_score, 2)}
