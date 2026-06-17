import { readFileSync, statSync } from 'node:fs';

const requiredFiles = ['index.html', 'src/main.js', 'src/styles.css'];
const requiredPhrases = [
  'Trade only explosive premium expansion moves.',
  'Volume Explosion',
  'Delta Acceleration',
  'Aggressive marketable limit order',
  'Skip 95% of signals',
];

for (const file of requiredFiles) {
  const stats = statSync(file);
  if (!stats.isFile() || stats.size === 0) {
    throw new Error(`${file} is missing or empty`);
  }
}

const html = readFileSync('index.html', 'utf8');
for (const phrase of requiredPhrases) {
  if (!html.includes(phrase)) {
    throw new Error(`Missing required phrase: ${phrase}`);
  }
}

console.log('Static site check passed.');
