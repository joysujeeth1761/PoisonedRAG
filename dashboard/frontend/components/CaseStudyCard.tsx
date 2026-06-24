'use client';

import { AttackExample } from '@/lib/fallbackData';

interface CaseStudyCardProps {
  examples: AttackExample[];
}

const FAILURE_MODES = [
  {
    title: 'Clean text retrieved instead',
    description:
      'The malicious text P failed to rank in the top-k retrieved contexts. The LLM answered correctly using benign corpus passages.',
  },
  {
    title: 'Malicious text contains correct answer',
    description:
      'Even though poison was retrieved, the generated paragraph I inadvertently included the correct answer, causing the attack to fail.',
  },
];

export default function CaseStudyCard({ examples }: CaseStudyCardProps) {
  return (
    <div className="glass-card p-4">
      <h3 className="text-sm font-semibold text-cyan-glow mb-4 uppercase tracking-wider">
        Case Studies & Failure Analysis
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-96 overflow-y-auto pr-2">
        {examples.map((ex, i) => (
          <div key={i} className="bg-navy-900/60 border border-navy-700/50 rounded-lg p-4 text-sm">
            <div className="mb-2">
              <span className="text-[10px] uppercase text-slate-500">Target Question</span>
              <p className="text-slate-200 font-medium">{ex.target_question}</p>
            </div>
            <div className="grid grid-cols-2 gap-2 mb-2">
              <div>
                <span className="text-[10px] uppercase text-emerald-500">Correct</span>
                <p className="text-emerald-400">{ex.correct_answer}</p>
              </div>
              <div>
                <span className="text-[10px] uppercase text-red-400">Target (Wrong)</span>
                <p className="text-red-400">{ex.target_answer}</p>
              </div>
            </div>
            <div>
              <span className="text-[10px] uppercase text-amber-500">Malicious Text P</span>
              <p className="text-slate-400 text-xs mt-1 line-clamp-3">{ex.malicious_text}</p>
            </div>
            {ex.failure_mode && (
              <div className="mt-2 pt-2 border-t border-navy-700">
                <span className="text-[10px] uppercase text-orange-400">Why it failed?</span>
                <p className="text-xs text-slate-500">{ex.failure_mode}</p>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        {FAILURE_MODES.map((fm) => (
          <div key={fm.title} className="bg-red-500/5 border border-red-500/20 rounded-lg p-3">
            <h4 className="text-xs font-semibold text-red-400 uppercase mb-1">{fm.title}</h4>
            <p className="text-xs text-slate-400">{fm.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
