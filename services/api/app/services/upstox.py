class UpstoxGateway:
    """Integration boundary for OAuth, Websocket V3, orders, funds, positions, holdings, option chain, and historical APIs."""

    def oauth_authorize_url(self) -> str:
        return "https://api.upstox.com/v2/login/authorization/dialog"

    async def stream_market_data(self) -> None:
        """Connect to Upstox Websocket V3 and publish ticks into Redis-backed scanners."""
        raise NotImplementedError("Wire Upstox Websocket V3 credentials before live streaming.")

    async def place_marketable_limit_order(self, instrument_key: str, quantity: int, side: str, limit_price: float) -> dict:
        """Place aggressive marketable limit orders after the risk engine grants permission."""
        return {"instrument_key": instrument_key, "quantity": quantity, "side": side, "limit_price": limit_price, "status": "dry_run"}
