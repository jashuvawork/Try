# NexusQuant Explosive Hunter V3

Production-grade AI trading platform blueprint and implementation scaffold for trading only the highest-conviction explosive NIFTY and SENSEX option premium expansion opportunities.

## Mission

- Ignore normal scalps, low-quality trades, range-bound conditions, and lunch-session chop.
- Trade only explosive option moves with probability of large premium expansion.
- Capital model: ₹5,00,000, 1–3 trades per day, minimum daily objective ₹20,000–₹30,000.
- Skip 95% of opportunities; quality over quantity.

## Monorepo Layout

- `apps/web`: Next.js 15 + TypeScript + TailwindCSS + Framer Motion + Recharts + Zustand dashboard.
- `services/api`: FastAPI backend with explosive scanner, points predictor, risk, paper/live trading, Upstox, news, journal, and telemetry endpoints.
- `database`: PostgreSQL schema for signals, snapshots, trades, news, AI predictions, journals, reports, and learning samples.
- `infra`: Deployment and observability blueprint for Vercel, Railway, PostgreSQL, Redis, AWS EC2/S3/CloudWatch, and alert channels.

## Validation

```bash
npm run validate
```

The validation script checks that the platform scaffold includes the required frontend modules, backend routes, database tables, risk rules, and explosive scoring engines.

## Build-Everything Strategy Implemented

The scaffold now includes deterministic production-path engines for the screenshot-style move:

1. Upstox-ready market context and live tick integration boundary.
2. 1-minute option candle model for premium, volume, OI, bid, and ask state.
3. Premium acceleration, volume explosion, 15-minute structure break, option-chain bias, delta/OI/gamma, order-flow, and news-shock engines.
4. Expected-points predictor for +5 through +100 premium-point expansion.
5. Late Session Premium Expansion Spike setup detection for 14:30–15:25 IST.
6. Risk engine, paper-trade simulator, live-trade guard, expanded database tables, and frontend roadmap/scanner cards.

Live capital deployment must remain disabled until Upstox credentials, paper-trade analytics, broker compliance checks, and production monitoring are configured.
