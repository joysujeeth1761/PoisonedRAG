'use client';

import { useState } from 'react';
import { DEFENSE_INFO } from '@/lib/fallbackData';

interface DefenseToggleProps {
  onDefenseChange: (defense: string | null, expansionK?: number) => void;
  baselineAsr?: number;
  currentAsr?: number;
}

export default function DefenseToggle({ onDefenseChange, baselineAsr = 0.97, currentAsr }: DefenseToggleProps) {
  const [active, setActive] = useState<string | null>(null);
  const [expansionK, setExpansionK] = useState(20);

  const handleToggle = (defense: string) => {
    const next = active === defense ? null : defense;
    setActive(next);
    onDefenseChange(next, defense === 'expansion' ? expansionK : undefined);
  };

  const defenses = Object.entries(DEFENSE_INFO) as [string, { label: string; asrDrop: number }][];

  return (
    <div className="glass-card p-4 h-full">
      <h3 className="text-sm font-semibold text-cyan-glow mb-3 uppercase tracking-wider">
        Defense Simulation
      </h3>

      <div className="space-y-3">
        {defenses.map(([key, info]) => (
          <div key={key} className="flex items-center justify-between bg-navy-900/50 rounded-lg p-3">
            <div>
              <div className="text-sm font-medium">{info.label}</div>
              <div className="text-[10px] text-slate-500">
                ASR drop: ~{(info.asrDrop * 100).toFixed(0)}%
              </div>
            </div>
            <button
              onClick={() => handleToggle(key)}
              className={`relative w-12 h-6 rounded-full transition-colors ${
                active === key ? 'bg-cyan-glow/30' : 'bg-navy-700'
              }`}
            >
              <span
                className={`absolute top-0.5 w-5 h-5 rounded-full transition-all ${
                  active === key ? 'left-6 bg-cyan-glow' : 'left-0.5 bg-slate-400'
                }`}
              />
            </button>
          </div>
        ))}
      </div>

      {active === 'expansion' && (
        <div className="mt-4">
          <label className="text-xs text-slate-400">Expansion k: {expansionK}</label>
          <input
            type="range"
            min={10}
            max={50}
            value={expansionK}
            onChange={(e) => {
              const val = Number(e.target.value);
              setExpansionK(val);
              onDefenseChange('expansion', val);
            }}
            className="w-full accent-emerald-500 mt-1"
          />
        </div>
      )}

      {active === 'perplexity' && (
        <div className="mt-4 p-3 bg-navy-900 rounded-lg">
          <p className="text-xs text-slate-400 mb-2">Perplexity Detection AUC</p>
          <svg viewBox="0 0 200 80" className="w-full">
            <path
              d="M10,70 Q50,65 80,50 T170,15"
              fill="none"
              stroke="#10b981"
              strokeWidth="2"
            />
            <text x="170" y="12" fill="#10b981" fontSize="10">AUC ≈ 0.82</text>
          </svg>
        </div>
      )}

      <div className="mt-4 grid grid-cols-2 gap-2 text-center">
        <div className="bg-navy-900 rounded-lg p-2">
          <div className="text-lg font-bold text-red-400">{(baselineAsr * 100).toFixed(0)}%</div>
          <div className="text-[10px] text-slate-500">Baseline ASR</div>
        </div>
        <div className="bg-navy-900 rounded-lg p-2">
          <div className="text-lg font-bold text-emerald-400">
            {currentAsr != null ? `${(currentAsr * 100).toFixed(0)}%` : '—'}
          </div>
          <div className="text-[10px] text-slate-500">Defended ASR</div>
        </div>
      </div>
    </div>
  );
}
