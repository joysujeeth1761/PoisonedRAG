'use client';

import { useState, useEffect, useCallback } from 'react';
import Controls from '@/components/Controls';
import RAGFlowChart from '@/components/RAGFlowChart';
import AttackPipeline from '@/components/AttackPipeline';
import MetricsPanel from '@/components/MetricsPanel';
import BaselineChart from '@/components/BaselineChart';
import DefenseToggle from '@/components/DefenseToggle';
import CaseStudyCard from '@/components/CaseStudyCard';
import { useAttackData } from '@/hooks/useAttackData';
import { FALLBACK_ATTACK } from '@/lib/fallbackData';

export default function Dashboard() {
  const [dataset, setDataset] = useState('nq');
  const [llm, setLlm] = useState('palm2');
  const [n, setN] = useState(5);
  const [k, setK] = useState(5);
  const [attackType, setAttackType] = useState('blackbox');
  const [attackActive, setAttackActive] = useState(false);

  const { loading, metrics, baselines, asrSweep, error, runAttack, fetchBaselines, fetchAsrSweep, runDefense } =
    useAttackData();

  const handleLaunch = useCallback(async () => {
    setAttackActive(true);
    await runAttack({ dataset, attack_type: attackType, n, k, llm });
    await fetchBaselines(dataset, llm, n, k);
    await fetchAsrSweep(dataset, llm, attackType);
  }, [dataset, attackType, n, k, llm, runAttack, fetchBaselines, fetchAsrSweep]);

  useEffect(() => {
    handleLaunch();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const data = metrics || FALLBACK_ATTACK;
  const decomp = data.decomposition;

  const handleDefense = (defense: string | null, expansionK?: number) => {
    if (!defense) {
      handleLaunch();
      return;
    }
    runDefense({ dataset, attack_type: attackType, n, k, llm, defense, expansion_k: expansionK });
  };

  return (
    <div className="min-h-screen bg-navy-950">
      <header className="border-b border-navy-700/50 bg-navy-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-glow to-emerald-400 bg-clip-text text-transparent">
              PoisonedRAG
            </h1>
            <p className="text-xs text-slate-500">Attack & Defense Visualizer</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs text-slate-400">USENIX Security &apos;25</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        <Controls
          dataset={dataset}
          setDataset={setDataset}
          llm={llm}
          setLlm={setLlm}
          n={n}
          setN={setN}
          k={k}
          setK={setK}
          attackType={attackType}
          setAttackType={setAttackType}
          loading={loading}
          onLaunch={handleLaunch}
        />

        {error && (
          <div className="text-xs text-amber-400 bg-amber-400/10 border border-amber-400/20 rounded-lg px-3 py-2">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <RAGFlowChart active={attackActive} maliciousInTopK={Math.min(n, k)} />
          <AttackPipeline
            retrievalPart={decomp?.S_retrieval}
            generationPart={decomp?.I_generation}
            fullText={decomp?.P_full}
            generationPrompt={decomp?.generation_prompt}
          />
        </div>

        <MetricsPanel metrics={data.metrics} asrSweep={asrSweep} loading={loading} />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <BaselineChart baselines={baselines} loading={loading} />
          <DefenseToggle
            onDefenseChange={handleDefense}
            baselineAsr={FALLBACK_ATTACK.metrics.asr}
            currentAsr={data.metrics.asr}
          />
        </div>

        <CaseStudyCard examples={data.examples} />
      </main>

      <footer className="border-t border-navy-700/50 mt-8 py-4 text-center text-xs text-slate-600">
        Based on PoisonedRAG (Zou et al., USENIX Security 2025) ·{' '}
        <a href="https://arxiv.org/abs/2402.07867" className="text-cyan-dim hover:text-cyan-glow" target="_blank" rel="noreferrer">
          arXiv:2402.07867
        </a>
      </footer>
    </div>
  );
}
