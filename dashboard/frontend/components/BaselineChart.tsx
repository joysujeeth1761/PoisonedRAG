'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  Legend,
} from 'recharts';
import { BASELINE_LABELS } from '@/lib/fallbackData';

interface BaselineChartProps {
  baselines: { name: string; asr: number; f1_score: number }[];
  loading?: boolean;
}

const COLORS: Record<string, string> = {
  naive: '#64748b',
  prompt_injection: '#6366f1',
  disinformation: '#8b5cf6',
  corpus: '#ec4899',
  gcg: '#f97316',
  poisonedrag: '#fbbf24',
};

export default function BaselineChart({ baselines, loading }: BaselineChartProps) {
  const data = baselines.map((b) => ({
    ...b,
    label: BASELINE_LABELS[b.name] || b.name,
    asrPct: b.asr * 100,
    f1Pct: b.f1_score * 100,
  }));

  if (loading) {
    return (
      <div className="glass-card p-4 h-full">
        <div className="skeleton h-64" />
      </div>
    );
  }

  return (
    <div className="glass-card p-4 h-full">
      <h3 className="text-sm font-semibold text-cyan-glow mb-3 uppercase tracking-wider">
        Baseline Comparison
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 40 }}>
          <XAxis
            dataKey="label"
            tick={{ fill: '#64748b', fontSize: 9 }}
            angle={-25}
            textAnchor="end"
            interval={0}
          />
          <YAxis
            tick={{ fill: '#64748b', fontSize: 10 }}
            domain={[0, 100]}
            tickFormatter={(v) => `${v}%`}
          />
          <Tooltip
            contentStyle={{ background: '#151d35', border: '1px solid #1a2540', borderRadius: 8 }}
            formatter={(value: number, name: string) => [
              `${value.toFixed(1)}%`,
              name === 'asrPct' ? 'ASR' : 'F1',
            ]}
          />
          <Legend wrapperStyle={{ fontSize: 11 }} />
          <Bar dataKey="asrPct" name="ASR" radius={[4, 4, 0, 0]}>
            {data.map((entry) => (
              <Cell
                key={entry.name}
                fill={COLORS[entry.name] || '#64748b'}
                stroke={entry.name === 'poisonedrag' ? '#fbbf24' : undefined}
                strokeWidth={entry.name === 'poisonedrag' ? 2 : 0}
              />
            ))}
          </Bar>
          <Bar dataKey="f1Pct" name="F1" fill="#00d4ff" opacity={0.4} radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-[10px] text-amber-400/80 mt-1 flex items-center gap-1">
        ★ PoisonedRAG achieves highest ASR across all baselines
      </p>
    </div>
  );
}
