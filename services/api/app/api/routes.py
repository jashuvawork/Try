from fastapi import APIRouter

from services.api.app.models.schemas import EngineScore, RiskState
from services.api.app.services.scoring import qualify_signal

router = APIRouter()


@router.get("/explosive-scanner")
def explosive_scanner():
    engines = EngineScore(
        premium_acceleration=94,
        volume_explosion=92,
        delta_velocity=88,
        oi_velocity=86,
        gamma_pressure=83,
        news_shock=91,
        spread_quality=96,
    )
    return qualify_signal("NIFTY", "NIFTY 50 CE", "BULLISH", engines, 94, 22, True, True)


@router.get("/points-predictor")
def points_predictor(current_premium: float = 68):
    return {
        "current_premium": current_premium,
        "minimum_trade_threshold_points": 15,
        "targets": {"+5": 98, "+10": 95, "+15": 92, "+20": 90, "+30": 75, "+50": 50, "+75": 28, "+100": 12},
    }


@router.get("/orderflow")
def orderflow():
    return {"buyer_aggression": 88, "seller_aggression": 31, "bid_volume": 420000, "ask_volume": 770000, "imbalance_score": 84}


@router.get("/news")
def news():
    return {"classification": "Bullish", "impact_score": 91, "tracked": ["RBI", "Fed", "Inflation", "War", "Budget", "Breaking headlines"]}


@router.get("/optionchain")
def optionchain():
    return {"pcr": 1.18, "call_writing": "Falling", "put_writing": "Rising", "long_buildup": True, "short_covering": True, "bullish_score": 87, "bearish_score": 22, "neutral_score": 12}


@router.get("/greeks")
def greeks():
    return {"delta_velocity": 88, "gamma_pressure": 83, "delta_acceleration": 2.4, "dealer_positioning": "squeeze-risk"}


@router.get("/risk", response_model=RiskState)
def risk():
    return RiskState()


@router.post("/paper")
def paper_trade():
    return {"status": "recorded", "requirement": "100 paper trades, PF > 2, win rate > 55%, positive expectancy"}


@router.post("/live")
def live_trade():
    return {"status": "guarded", "execution": "marketable_limit", "stop_loss": "5-6 premium points", "scale_out": ["30% at +10", "30% at +20", "trail runner"]}


@router.get("/journal")
def journal():
    return {"fields": ["setup", "screenshots", "engine_scores", "entry", "exit", "pnl", "lesson", "learning_sample_id"]}


@router.get("/telemetry")
def telemetry():
    return {"cloud": "AWS EC2", "logs": "structured_json", "monitoring": "CloudWatch", "alerts": ["Telegram", "Discord", "Email"], "deployments": {"frontend": "Vercel", "backend": "Railway"}}
