'use client';

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

const expectedPoints = [
  { target: '+5', probability: 98 },
  { target: '+10', probability: 95 },
  { target: '+15', probability: 92 },
  { target: '+20', probability: 90 },
  { target: '+30', probability: 75 },
  { target: '+50', probability: 50 },
  { target: '+75', probability: 28 },
  { target: '+100', probability: 12 },
];

export function ProbabilityChart() {
  return (
    <div className="h-72 rounded-3xl border border-slate-800 bg-slate-950/70 p-4">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={expectedPoints} margin={{ left: -20, right: 8, top: 12, bottom: 0 }}>
          <defs>
            <linearGradient id="probability" x1="0" x2="0" y1="0" y2="1">
              <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#22d3ee" stopOpacity={0.05} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis dataKey="target" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" domain={[0, 100]} />
          <Tooltip contentStyle={{ background: '#020617', border: '1px solid #1e293b', borderRadius: 16 }} />
          <Area type="monotone" dataKey="probability" stroke="#22d3ee" fill="url(#probability)" strokeWidth={3} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
