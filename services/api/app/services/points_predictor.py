def predict_expected_points(premium_acceleration: float, volume_multiple: float, delta_velocity: float, oi_velocity: float, spread_score: float, news_score: float) -> dict:
    impulse = premium_acceleration * 0.28 + min(volume_multiple * 18, 100) * 0.22 + delta_velocity * 0.18 + oi_velocity * 0.14 + spread_score * 0.08 + news_score * 0.10
    targets = {}
    for points, penalty in [(5, 0), (10, 4), (15, 8), (20, 13), (30, 24), (50, 43), (75, 61), (100, 76)]:
        targets[f"+{points}"] = round(max(1, min(99, impulse - penalty)), 2)
    expected_move = max((points for points in [5, 10, 15, 20, 30, 50, 75, 100] if targets[f"+{points}"] >= 70), default=0)
    return {"impulse_score": round(impulse, 2), "expected_move_points": expected_move, "targets": targets}
