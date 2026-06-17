from fastapi import APIRouter

from services.api.app.models.schemas import RiskState
from services.api.app.services.market_state import sample_context
from services.api.app.services.paper_trading import simulate_paper_trade
from services.api.app.services.risk import evaluate_risk
from services.api.app.services.scanner import scan_context
from services.api.app.services.upstox import UpstoxGateway

router = APIRouter()


def latest_scan() -> dict:
    return scan_context(sample_context())


@router.get("/explosive-scanner")
def explosive_scanner():
    return latest_scan()


@router.get("/points-predictor")
def points_predictor():
    return latest_scan()["points_predictor"]


@router.get("/orderflow")
def orderflow():
    return latest_scan()["order_flow"]


@router.get("/news")
def news():
    return latest_scan()["news"]


@router.get("/optionchain")
def optionchain():
    return latest_scan()["option_chain"]


@router.get("/greeks")
def greeks():
    return latest_scan()["greeks"]


@router.get("/risk", response_model=RiskState)
def risk(daily_pnl: int = 0, consecutive_losses: int = 0):
    return evaluate_risk(daily_pnl=daily_pnl, consecutive_losses=consecutive_losses)


@router.post("/paper")
def paper_trade():
    scan = latest_scan()
    return {"status": "simulated", "signal": scan["signal"], "trade": simulate_paper_trade(scan["signal"]["expected_move_points"] + 68)}


@router.post("/live")
def live_trade():
    permission = evaluate_risk(paper_trades=100, profit_factor=2.2, win_rate=58, live_requested=True)
    if permission.trade_permission == "NO TRADE":
        return {"status": "blocked", "risk": permission.model_dump()}
    dry_run = UpstoxGateway().place_marketable_limit_order
    return {"status": "guarded", "execution": "marketable_limit", "risk": permission.model_dump(), "upstox_boundary": dry_run.__name__, "stop_loss": "5-6 premium points", "scale_out": ["30% at +10", "30% at +20", "trail runner"]}


@router.get("/journal")
def journal():
    return {"fields": ["setup", "screenshots", "engine_scores", "entry", "exit", "pnl", "lesson", "learning_sample_id"], "learning_loop": ["paper trades", "live trades", "winning trades", "losing trades", "weight updates"]}


@router.get("/telemetry")
def telemetry():
    return {"cloud": "AWS EC2", "logs": "structured_json", "monitoring": "CloudWatch", "alerts": ["Telegram", "Discord", "Email"], "deployments": {"frontend": "Vercel", "backend": "Railway"}, "websocket": {"provider": "Upstox Websocket V3", "status": "ready_for_credentials", "last_tick_age_ms": None}}
