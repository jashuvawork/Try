from services.api.app.services.market_state import MarketContext


def score_news_shock(context: MarketContext) -> dict:
    aligned = (context.news_classification == "Bearish" and "BEARISH" in context.direction) or (context.news_classification == "Bullish" and "BULLISH" in context.direction)
    return {"classification": context.news_classification, "impact_score": context.news_impact, "aligned": aligned, "tracked": ["RBI", "Fed", "Inflation", "War", "Budget", "Breaking headlines"]}
