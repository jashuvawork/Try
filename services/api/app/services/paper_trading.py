def simulate_paper_trade(entry: float, direction: str = "LONG_OPTION") -> dict:
    stop = round(entry - 6, 2)
    return {"mode": "paper", "entry": entry, "stop_loss": stop, "scale_out": [{"points": 10, "quantity_pct": 30}, {"points": 20, "quantity_pct": 30}], "runner": "trail until momentum, delta, volume, gamma, or OI dies", "direction": direction}
