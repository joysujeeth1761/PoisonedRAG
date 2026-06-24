'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
} from 'recharts';
import { Metrics } from '@/lib/fallbackData';

interface MetricsPanelProps {
  metrics: Metrics | null;
  asrSweep: { n: number; asr: number }[];
  loading: boolean;
}

function ASRGauge({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const circumference = 2 * Math.PI * 45;
  const offset = circumference - (value * circumference);

  return (
    <div className="relative w-32 h-32 mx-auto">
      <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
        <circle cx="50" cy="50" r="45" fill="none" stroke="#1a2540" strokeWidth="8" />
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          stroke="#00d4ff"
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-1000"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-2xl font-bold text-cyan-glow">{pct}%</span>
        <span className="text-[10px] text-slate-400 uppercase">ASR</span>
      </div>
    </div>
  );
}

function MetricBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="mb-2">
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span style={{ color }}>{(value * 100).toFixed(1)}%</span>
      </div>
      <div className="h-2 bg-navy-900 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${value * 100}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

export default function MetricsPanel({ metrics, asrSweep, loading }: MetricsPanelProps) {
  if (loading && !metrics) {
    return (
      <div className="glass-card p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton h-32" />
          ))}
        </div>
      </div>
    );
  }

  const m = metrics || { asr: 0, f1_score: 0, precision: 0, recall: 0, queries_avg: 0, runtime_avg: 0 };

  const f1Data = [
    { name: 'Precision', value: m.precision },
    { name: 'Recall', value: m.recall },
    { name: 'F1', value: m.f1_score },
  ];

  return (
    <div className="glass-card p-4">
      <h3 className="text-sm font-semibold text-cyan-glow mb-4 uppercase tracking-wider">Metrics Dashboard</h3>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="flex flex-col items-center justify-center">
          <ASRGauge value={m.asr} />
          <p className="text-xs text-slate-500 mt-2 text-center">Attack Success Rate</p>
        </div>

        <div className="flex flex-col justify-center">
          <MetricBar label="Precision" value={m.precision} color="#00d4ff" />
          <MetricBar label="Recall" value={m.recall} color="#10b981" />
          <MetricBar label="F1-Score" value={m.f1_score} color="#fbbf24" />
        </div>

        <div className="flex flex-col gap-3 justify-center">
          <div className="bg-navy-900 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-cyan-glow">{m.queries_avg.toFixed(1)}</div>
            <div className="text-[10px] text-slate-400 uppercase">Avg Queries / Text</div>
          </div>
          <div className="bg-navy-900 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-emerald-400">{m.runtime_avg.toFixed(1)}s</div>
            <div className="text-[10px] text-slate-400 uppercase">Runtime</div>
          </div>
        </div>

        <div>
          <p className="text-xs text-slate-400 mb-2 uppercase">ASR vs N (diminishing returns)</p>
          <ResponsiveContainer width="100%" height={140}>
            <LineChart data={asrSweep}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1a2540" />
              <XAxis dataKey="n" tick={{ fill: '#64748b', fontSize: 10 }} />
              <YAxis domain={[0.6, 1]} tick={{ fill: '#64748b', fontSize: 10 }} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
              <Tooltip
                contentStyle={{ background: '#151d35', border: '1px solid #1a2540', borderRadius: 8 }}
                formatter={(v: number) => [`${(v * 100).toFixed(1)}%`, 'ASR']}
              />
              <Line type="monotone" dataKey="asr" stroke="#00d4ff" strokeWidth={2} dot={{ fill: '#00d4ff', r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-4 hidden md:block">
        <ResponsiveContainer width="100%" height={80}>
          <BarChart data={f1Data} layout="vertical">
            <XAxis type="number" domain={[0, 1]} tick={{ fill: '#64748b', fontSize: 10 }} />
            <YAxis type="category" dataKey="name" tick={{ fill: '#64748b', fontSize: 10 }} width={70} />
            <Bar dataKey="value" fill="#00d4ff" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
