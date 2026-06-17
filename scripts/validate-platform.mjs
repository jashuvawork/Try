import { readFileSync, statSync } from 'node:fs';

const requiredFiles = [
  'apps/web/app/page.tsx',
  'apps/web/components/HunterDashboard.tsx',
  'apps/web/components/ProbabilityChart.tsx',
  'apps/web/lib/platform.ts',
  'services/api/app/main.py',
  'services/api/app/api/routes.py',
  'services/api/app/services/scoring.py',
  'services/api/app/services/upstox.py',
  'database/schema.sql',
  'infra/deployment.md',
];

const requiredApiRoutes = [
  '/api/explosive-scanner',
  '/api/points-predictor',
  '/api/orderflow',
  '/api/news',
  '/api/optionchain',
  '/api/greeks',
  '/api/risk',
  '/api/paper',
  '/api/live',
  '/api/journal',
  '/api/telemetry',
];

const requiredTables = [
  'signals',
  'market_snapshots',
  'option_chain_snapshots',
  'paper_trades',
  'live_trades',
  'news_events',
  'ai_predictions',
  'trade_journal',
  'daily_reports',
  'learning_samples',
];

for (const file of requiredFiles) {
  const stats = statSync(file);
  if (!stats.isFile() || stats.size === 0) throw new Error(`${file} is missing or empty`);
}

const routes = readFileSync('services/api/app/api/routes.py', 'utf8');
for (const route of requiredApiRoutes) {
  const routePath = route.replace('/api', '');
  if (!routes.includes(`"${routePath}"`)) throw new Error(`Missing backend route ${route}`);
}

const schema = readFileSync('database/schema.sql', 'utf8');
for (const table of requiredTables) {
  if (!schema.includes(`CREATE TABLE ${table}`)) throw new Error(`Missing table ${table}`);
}

const dashboard = readFileSync('apps/web/components/HunterDashboard.tsx', 'utf8');
for (const phrase of ['NIFTY & SENSEX', '₹5,00,000', 'skips 95%', 'Expected points predictor']) {
  if (!dashboard.includes(phrase)) throw new Error(`Missing dashboard phrase: ${phrase}`);
}

const scoring = readFileSync('services/api/app/services/scoring.py', 'utf8');
for (const threshold of ['probability <= 90', 'ai_confidence <= 90', 'expected_move_points <= 15']) {
  if (!scoring.includes(threshold)) throw new Error(`Missing scoring threshold: ${threshold}`);
}

console.log('NexusQuant platform scaffold validation passed.');
