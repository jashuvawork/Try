from services.api.app.models.schemas import EngineScore
from services.api.app.services.engines.delta_oi_gamma import score_delta_oi_gamma
from services.api.app.services.engines.news_shock import score_news_shock
from services.api.app.services.engines.option_chain_bias import score_option_chain_bias
from services.api.app.services.engines.order_flow import score_order_flow
from services.api.app.services.engines.premium_acceleration import score_premium_acceleration
from services.api.app.services.engines.structure_break import score_structure_break
from services.api.app.services.engines.volume_explosion import score_volume_explosion
from services.api.app.services.market_state import MarketContext
from services.api.app.services.points_predictor import predict_expected_points
from services.api.app.services.scoring import qualify_signal
from services.api.app.services.setups.late_session_expansion import detect_late_session_expansion


def scan_context(context: MarketContext) -> dict:
    premium = score_premium_acceleration(context)
    volume = score_volume_explosion(context)
    structure = score_structure_break(context)
    chain = score_option_chain_bias(context)
    order_flow = score_order_flow(context)
    news = score_news_shock(context)
    greeks = score_delta_oi_gamma(context)
    momentum_score = round((premium["score"] * 0.45 + greeks["delta_velocity"] * 0.35 + volume["score"] * 0.20), 2)
    setup = detect_late_session_expansion(context, volume["volume_multiple"], premium["score"], momentum_score, structure["break_direction"])
    points = predict_expected_points(premium["score"], volume["volume_multiple"], greeks["delta_velocity"], greeks["oi_velocity"], order_flow["spread_score"], news["impact_score"])
    engines = EngineScore(
        premium_acceleration=premium["score"],
        volume_explosion=volume["score"],
        delta_velocity=greeks["delta_velocity"],
        oi_velocity=greeks["oi_velocity"],
        gamma_pressure=greeks["gamma_pressure"],
        news_shock=news["impact_score"],
        spread_quality=order_flow["spread_score"],
    )
    signal = qualify_signal(context.symbol, context.instrument, context.direction, engines, context.ai_confidence, points["expected_move_points"], chain["aligned"], news["aligned"])
    if not setup["valid"]:
        signal.decision = "SKIP"
        signal.rejection_reason = f"{signal.rejection_reason + '; ' if signal.rejection_reason else ''}Named setup not valid"
    return {"signal": signal.model_dump(), "premium": premium, "volume": volume, "structure": structure, "option_chain": chain, "order_flow": order_flow, "news": news, "greeks": greeks, "momentum_score": momentum_score, "points_predictor": points, "setup": setup}
