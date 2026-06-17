export const capitalProfile = {
  capital: '₹5,00,000',
  riskPerTrade: '₹2,500',
  dailyLossLimit: '₹10,000',
  dailyTarget: '₹25,000',
  stretchTarget: '₹30,000',
  maxTrades: '1–3',
};

export const engineWeights = [
  { name: 'Premium Acceleration', weight: 25, score: 94 },
  { name: 'Volume Explosion', weight: 20, score: 92 },
  { name: 'Delta Velocity', weight: 15, score: 88 },
  { name: 'OI Velocity', weight: 15, score: 86 },
  { name: 'Gamma Pressure', weight: 10, score: 83 },
  { name: 'News Shock', weight: 10, score: 76 },
  { name: 'Spread Quality', weight: 5, score: 98 },
];

export const scannerSnapshot = {
  instrument: 'NIFTY 23850 PE 16JUN26',
  setup: 'Late Session Premium Expansion Spike',
  premium: 68,
  decision: 'TRADE',
  expectedMove: 30,
  volumeMultiple: 3.18,
  previous15mHigh: 97.5,
  momentumScore: 92,
  riskStatus: 'A+',
  skipRateTarget: '95%',
};

export const entryRules = [
  'Explosive Probability > 90',
  'AI Confidence > 90',
  'Premium Acceleration > 85',
  'Volume Explosion > 85 and volume > 3× previous 5-minute average',
  'Delta Velocity > 80',
  'OI Velocity > 80',
  'Spread Score > 80',
  'News Score aligned',
  'Option Chain Bias aligned',
  'Previous 15-minute structure break confirmed',
  'Expected move exceeds 15 points',
];

export const modules = [
  'Explosive Scanner',
  'Explosive Probability Dashboard',
  'Expected Points Predictor',
  'Option Chain Bias',
  'Delta Velocity',
  'Gamma Positioning',
  'OI Velocity',
  'Volume Explosion',
  'News Shock Monitor',
  'Trade Journal',
  'Paper Trading',
  'Live Trading',
  'Risk Engine',
  'AI Analytics',
  'Infrastructure Telemetry',
];

export const implementationRoadmap = [
  'Upstox Websocket V3 tick ingestion',
  '1-minute option candle builder',
  'Premium acceleration and 3× volume explosion engines',
  '15-minute structure-break detector',
  'Option-chain PCR/OI bias engine',
  'Expected-points predictor',
  'Risk and paper-trading gates before live trading',
];
