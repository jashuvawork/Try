from services.api.app.models.schemas import EngineScore, ExplosiveSignal

WEIGHTS = {
    "premium_acceleration": 0.25,
    "volume_explosion": 0.20,
    "delta_velocity": 0.15,
    "oi_velocity": 0.15,
    "gamma_pressure": 0.10,
    "news_shock": 0.10,
    "spread_quality": 0.05,
}


def weighted_probability(score: EngineScore) -> float:
    return round(sum(getattr(score, key) * weight for key, weight in WEIGHTS.items()), 2)


def qualify_signal(symbol: str, instrument: str, direction: str, score: EngineScore, ai_confidence: float, expected_move_points: float, option_chain_aligned: bool, news_aligned: bool) -> ExplosiveSignal:
    probability = weighted_probability(score)
    blockers = []
    if probability <= 90:
        blockers.append("Explosive Probability must be > 90")
    if ai_confidence <= 90:
        blockers.append("AI Confidence must be > 90")
    if score.premium_acceleration <= 85:
        blockers.append("Premium Acceleration must be > 85")
    if score.volume_explosion <= 85:
        blockers.append("Volume Explosion must be > 85")
    if score.delta_velocity <= 80:
        blockers.append("Delta Velocity must be > 80")
    if score.oi_velocity <= 80:
        blockers.append("OI Velocity must be > 80")
    if score.spread_quality <= 80:
        blockers.append("Spread Score must be > 80")
    if not option_chain_aligned:
        blockers.append("Option Chain Bias not aligned")
    if not news_aligned:
        blockers.append("News Score not aligned")
    if expected_move_points <= 15:
        blockers.append("Expected move must exceed 15 points")

    decision = "TRADE" if not blockers else "SKIP"
    return ExplosiveSignal(
        symbol=symbol,
        instrument=instrument,
        direction=direction,
        explosive_probability=probability,
        trade_quality_score=round((probability + ai_confidence) / 2, 2),
        ai_confidence=ai_confidence,
        expected_move_points=expected_move_points,
        decision=decision,
        engines=score,
        rejection_reason="; ".join(blockers) if blockers else None,
    )
