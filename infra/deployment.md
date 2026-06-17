# NexusQuant Deployment Blueprint

## Frontend: Vercel
- Deploy `apps/web` as the Next.js 15 application.
- Configure API base URL, telemetry environment, and feature flags through Vercel environment variables.

## Backend: Railway
- Deploy `services/api` as the FastAPI service.
- Run with `uvicorn services.api.app.main:app --host 0.0.0.0 --port $PORT`.
- Configure Upstox OAuth, NewsAPI, Finnhub, PostgreSQL, Redis, Telegram, Discord, and email secrets.

## Database and Cache
- PostgreSQL stores signals, market snapshots, option-chain snapshots, paper trades, live trades, news events, AI predictions, journals, reports, and learning samples.
- Redis caches live Upstox Websocket V3 ticks, option-chain deltas, news shock state, and risk locks.

## AWS Cloud
- EC2 hosts optional local ML scoring workers and websocket fan-out services.
- S3 stores model artifacts, daily reports, journal exports, and replay datasets.
- CloudWatch receives structured JSON logs, latency metrics, error rates, trade-permission changes, and deployment events.

## Alerts
- Telegram, Discord, and email alerts fire for hard daily loss, two consecutive losses, live order failure, websocket disconnect, wide spread, and cloud degradation.
