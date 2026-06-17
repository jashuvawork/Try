from services.api.app.models.schemas import RiskState


def evaluate_risk(daily_pnl: int = 0, consecutive_losses: int = 0, paper_trades: int = 0, profit_factor: float = 0, win_rate: float = 0, live_requested: bool = False) -> RiskState:
    permission = "A+"
    if daily_pnl <= -10000 or consecutive_losses >= 2:
        permission = "NO TRADE"
    elif daily_pnl >= 25000:
        permission = "LOCK_PROFIT"
    elif live_requested and (paper_trades < 100 or profit_factor <= 2 or win_rate <= 55):
        permission = "NO TRADE"
    return RiskState(consecutive_losses=consecutive_losses, trade_permission=permission)
