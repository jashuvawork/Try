'use client';

import { motion } from 'framer-motion';
import { create } from 'zustand';
import { capitalProfile, engineWeights, entryRules, modules } from '../lib/platform';
import { ProbabilityChart } from './ProbabilityChart';

type HunterState = {
  session: 'CALM' | 'SELECTIVE' | 'AGGRESSIVE' | 'LOCK_PROFIT' | 'DEFENSIVE';
  permission: 'A+' | 'A' | 'B' | 'NO TRADE';
  explosiveProbability: number;
  aiConfidence: number;
  tradeQuality: number;
};

const useHunterStore = create<HunterState>(() => ({
  session: 'SELECTIVE',
  permission: 'A+',
  explosiveProbability: 93,
  aiConfidence: 94,
  tradeQuality: 92,
}));

export function HunterDashboard() {
  const state = useHunterStore();

  return (
    <main className="mx-auto min-h-screen w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <section className="grid min-h-[70vh] items-center gap-8 lg:grid-cols-[1.15fr_0.85fr]">
        <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <p className="mb-4 text-sm font-black uppercase tracking-[0.35em] text-cyan-300">Jashuva Explosive Hunter V3</p>
          <h1 className="max-w-5xl text-5xl font-black leading-[0.88] tracking-[-0.08em] text-white sm:text-7xl lg:text-8xl">
            NexusQuant trades only explosive NIFTY & SENSEX option expansions.
          </h1>
          <p className="mt-8 max-w-3xl text-lg leading-8 text-slate-300">
            Built for ₹5,00,000 capital, 1–3 trades per day, and ₹20,000–₹30,000 daily target discipline. The system skips 95% of setups and permits only the highest-conviction premium expansion opportunities.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            {['Ignore scalps', 'Reject chop', 'Demand >90 probability', 'Trade quality > quantity'].map((item) => (
              <span key={item} className="rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-2 text-sm font-bold text-cyan-100">{item}</span>
            ))}
          </div>
        </motion.div>

        <motion.aside initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.6, delay: 0.1 }} className="rounded-[2rem] border border-white/10 bg-white/[0.06] p-6 shadow-2xl shadow-cyan-950/40 backdrop-blur">
          <div className="grid grid-cols-3 gap-3">
            {[['Explosive Probability', state.explosiveProbability], ['AI Confidence', state.aiConfidence], ['Trade Quality', state.tradeQuality]].map(([label, value]) => (
              <div key={label} className="rounded-3xl bg-slate-950/80 p-4 text-center">
                <strong className="text-3xl font-black text-cyan-300">{value}</strong>
                <p className="mt-2 text-xs font-bold uppercase tracking-widest text-slate-400">{label}</p>
              </div>
            ))}
          </div>
          <div className="mt-5 rounded-3xl bg-emerald-400/10 p-5">
            <p className="text-sm font-bold uppercase tracking-[0.25em] text-emerald-300">Psychology Engine</p>
            <div className="mt-3 flex items-center justify-between text-2xl font-black"><span>{state.session}</span><span>{state.permission}</span></div>
          </div>
        </motion.aside>
      </section>

      <section className="grid gap-4 py-8 md:grid-cols-3 lg:grid-cols-6">
        {Object.entries(capitalProfile).map(([label, value]) => (
          <div key={label} className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
            <p className="text-xs font-bold uppercase tracking-widest text-slate-500">{label}</p>
            <strong className="mt-3 block text-2xl text-white">{value}</strong>
          </div>
        ))}
      </section>

      <section className="grid gap-6 py-8 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6">
          <p className="text-sm font-black uppercase tracking-[0.3em] text-rose-300">Explosive move engines</p>
          <div className="mt-5 space-y-4">
            {engineWeights.map((engine) => (
              <div key={engine.name}>
                <div className="mb-2 flex justify-between text-sm"><span>{engine.name}</span><span>{engine.weight}% weight · {engine.score}</span></div>
                <div className="h-3 overflow-hidden rounded-full bg-slate-800"><div className="h-full rounded-full bg-gradient-to-r from-cyan-300 to-rose-400" style={{ width: `${engine.score}%` }} /></div>
              </div>
            ))}
          </div>
        </div>
        <div>
          <p className="mb-4 text-sm font-black uppercase tracking-[0.3em] text-cyan-300">Expected points predictor</p>
          <ProbabilityChart />
        </div>
      </section>

      <section className="grid gap-6 py-8 lg:grid-cols-2">
        <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6">
          <h2 className="text-3xl font-black tracking-tight">Entry gate</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {entryRules.map((rule) => <div key={rule} className="rounded-2xl bg-white/[0.04] p-4 text-sm font-bold text-slate-200">{rule}</div>)}
          </div>
        </div>
        <div className="rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6">
          <h2 className="text-3xl font-black tracking-tight">Platform modules</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {modules.map((module) => <div key={module} className="rounded-2xl border border-slate-800 p-4 text-sm text-slate-300">{module}</div>)}
          </div>
        </div>
      </section>
    </main>
  );
}
