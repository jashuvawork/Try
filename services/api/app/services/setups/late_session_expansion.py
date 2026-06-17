from services.api.app.services.market_state import MarketContext


def detect_late_session_expansion(context: MarketContext, volume_multiple: float, premium_score: float, momentum_score: float, structure_break: str) -> dict:
    in_window = "14:30" <= context.session_time_ist <= "15:25"
    valid = in_window and volume_multiple >= 3 and premium_score > 85 and momentum_score > 80 and structure_break != "NONE"
    return {"setup": "Late Session Premium Expansion Spike", "valid": valid, "session_time_ist": context.session_time_ist, "requirements": {"time_window": in_window, "volume_multiple_ge_3": volume_multiple >= 3, "premium_score_gt_85": premium_score > 85, "momentum_score_gt_80": momentum_score > 80, "structure_break": structure_break != "NONE"}}
