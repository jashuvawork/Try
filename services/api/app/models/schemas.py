from pydantic import BaseModel, Field


class EngineScore(BaseModel):
    premium_acceleration: float = Field(ge=0, le=100)
    volume_explosion: float = Field(ge=0, le=100)
    delta_velocity: float = Field(ge=0, le=100)
    oi_velocity: float = Field(ge=0, le=100)
    gamma_pressure: float = Field(ge=0, le=100)
    news_shock: float = Field(ge=0, le=100)
    spread_quality: float = Field(ge=0, le=100)


class ExplosiveSignal(BaseModel):
    symbol: str
    instrument: str
    direction: str
    explosive_probability: float
    trade_quality_score: float
    ai_confidence: float
    expected_move_points: float
    decision: str
    engines: EngineScore
    rejection_reason: str | None = None


class RiskState(BaseModel):
    capital: int = 500000
    risk_per_trade: int = 2500
    daily_loss_limit: int = 10000
    daily_target: int = 25000
    stretch_target: int = 30000
    consecutive_losses: int = 0
    trade_permission: str = "A+"
