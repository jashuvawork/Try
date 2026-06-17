CREATE TABLE signals (
  id BIGSERIAL PRIMARY KEY,
  symbol TEXT NOT NULL,
  instrument TEXT NOT NULL,
  direction TEXT NOT NULL,
  explosive_probability NUMERIC(5,2) NOT NULL,
  trade_quality_score NUMERIC(5,2) NOT NULL,
  ai_confidence NUMERIC(5,2) NOT NULL,
  decision TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE market_snapshots (id BIGSERIAL PRIMARY KEY, symbol TEXT NOT NULL, price NUMERIC(12,2), volume BIGINT, momentum_score NUMERIC(5,2), captured_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE option_chain_snapshots (id BIGSERIAL PRIMARY KEY, symbol TEXT NOT NULL, expiry DATE, pcr NUMERIC(8,4), call_writing NUMERIC(12,2), put_writing NUMERIC(12,2), oi_shift JSONB, captured_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE paper_trades (id BIGSERIAL PRIMARY KEY, signal_id BIGINT REFERENCES signals(id), entry_price NUMERIC(10,2), exit_price NUMERIC(10,2), pnl NUMERIC(12,2), result TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE live_trades (id BIGSERIAL PRIMARY KEY, signal_id BIGINT REFERENCES signals(id), upstox_order_id TEXT, entry_price NUMERIC(10,2), exit_price NUMERIC(10,2), pnl NUMERIC(12,2), status TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE news_events (id BIGSERIAL PRIMARY KEY, source TEXT, headline TEXT NOT NULL, classification TEXT, impact_score NUMERIC(5,2), event_time TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE ai_predictions (id BIGSERIAL PRIMARY KEY, signal_id BIGINT REFERENCES signals(id), model_name TEXT, probability JSONB, confidence NUMERIC(5,2), created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE trade_journal (id BIGSERIAL PRIMARY KEY, trade_id BIGINT, mode TEXT CHECK (mode IN ('paper','live')), notes TEXT, discipline_score NUMERIC(5,2), lesson TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE daily_reports (id BIGSERIAL PRIMARY KEY, report_date DATE UNIQUE NOT NULL, gross_pnl NUMERIC(12,2), trades_taken INTEGER, skipped_signals INTEGER, win_rate NUMERIC(5,2), profit_factor NUMERIC(8,2), created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE learning_samples (id BIGSERIAL PRIMARY KEY, signal_id BIGINT REFERENCES signals(id), features JSONB NOT NULL, label TEXT, model_version TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
