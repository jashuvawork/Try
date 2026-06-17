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
  { name: 'Volume Explosion', weight: 20, score: 91 },
  { name: 'Delta Velocity', weight: 15, score: 87 },
  { name: 'OI Velocity', weight: 15, score: 84 },
  { name: 'Gamma Pressure', weight: 10, score: 78 },
  { name: 'News Shock', weight: 10, score: 82 },
  { name: 'Spread Quality', weight: 5, score: 96 },
];

export const entryRules = [
  'Explosive Probability > 90',
  'AI Confidence > 90',
  'Premium Acceleration > 85',
  'Volume Explosion > 85',
  'Delta Velocity > 80',
  'OI Velocity > 80',
  'Spread Score > 80',
  'News Score aligned',
  'Option Chain Bias aligned',
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
