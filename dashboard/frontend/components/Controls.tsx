'use client';

interface ControlsProps {
  dataset: string;
  setDataset: (v: string) => void;
  llm: string;
  setLlm: (v: string) => void;
  n: number;
  setN: (v: number) => void;
  k: number;
  setK: (v: number) => void;
  attackType: string;
  setAttackType: (v: string) => void;
  loading: boolean;
  onLaunch: () => void;
}

export default function Controls({
  dataset,
  setDataset,
  llm,
  setLlm,
  n,
  setN,
  k,
  setK,
  attackType,
  setAttackType,
  loading,
  onLaunch,
}: ControlsProps) {
  return (
    <div className="glass-card neon-border p-4 flex flex-wrap items-end gap-4">
      <div className="flex flex-col gap-1">
        <label className="text-xs text-cyan-glow/70 uppercase tracking-wider">Dataset</label>
        <select
          value={dataset}
          onChange={(e) => setDataset(e.target.value)}
          className="bg-navy-900 border border-navy-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-cyan-glow"
        >
          <option value="nq">Natural Questions (NQ)</option>
          <option value="hotpotqa">HotpotQA</option>
          <option value="msmarco">MS-MARCO</option>
        </select>
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-xs text-cyan-glow/70 uppercase tracking-wider">LLM</label>
        <select
          value={llm}
          onChange={(e) => setLlm(e.target.value)}
          className="bg-navy-900 border border-navy-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-cyan-glow"
        >
          <option value="palm2">PaLM 2</option>
          <option value="gpt4">GPT-4</option>
          <option value="llama2">LLaMA-2</option>
          <option value="vicuna">Vicuna</option>
        </select>
      </div>

      <div className="flex flex-col gap-1 min-w-[140px]">
        <label className="text-xs text-cyan-glow/70 uppercase tracking-wider">N (adv texts): {n}</label>
        <input
          type="range"
          min={1}
          max={10}
          value={n}
          onChange={(e) => setN(Number(e.target.value))}
          className="accent-cyan-glow"
        />
      </div>

      <div className="flex flex-col gap-1 min-w-[140px]">
        <label className="text-xs text-cyan-glow/70 uppercase tracking-wider">k (top-k): {k}</label>
        <input
          type="range"
          min={1}
          max={20}
          value={k}
          onChange={(e) => setK(Number(e.target.value))}
          className="accent-cyan-glow"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-xs text-cyan-glow/70 uppercase tracking-wider">Attack Mode</label>
        <div className="flex rounded-lg overflow-hidden border border-navy-700">
          <button
            onClick={() => setAttackType('blackbox')}
            className={`px-4 py-2 text-sm transition-colors ${
              attackType === 'blackbox' ? 'bg-cyan-glow/20 text-cyan-glow' : 'bg-navy-900 text-slate-400'
            }`}
          >
            Black-box
          </button>
          <button
            onClick={() => setAttackType('whitebox')}
            className={`px-4 py-2 text-sm transition-colors ${
              attackType === 'whitebox' ? 'bg-cyan-glow/20 text-cyan-glow' : 'bg-navy-900 text-slate-400'
            }`}
          >
            White-box
          </button>
        </div>
      </div>

      <button
        onClick={onLaunch}
        disabled={loading}
        className="ml-auto px-6 py-2.5 bg-gradient-to-r from-cyan-dim to-cyan-glow text-navy-950 font-semibold rounded-lg hover:opacity-90 disabled:opacity-50 transition-all flex items-center gap-2"
      >
        {loading ? (
          <>
            <span className="w-4 h-4 border-2 border-navy-950/30 border-t-navy-950 rounded-full animate-spin" />
            Running...
          </>
        ) : (
          <>Launch Attack</>
        )}
      </button>
    </div>
  );
}
